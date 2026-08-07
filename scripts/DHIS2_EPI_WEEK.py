import requests
from datetime import datetime, timedelta
import logging
import time
import os
from configparser import ConfigParser


class DHIS2Updater:
    # Server URL
    SERVER_URL = "" #CHANGE HERE

    # Script path folder
    RUNTIME_LOG_PATH = "" #CHANGE HERE

    # Log path file
    LOG_FILE = "dhis2_epiweek.log"

    # Page size for GET request. To prevent server 414 Request-URI Too Large
    PAGE_SIZE = '500'

    # AFP & Measles
    PROGRAM_IDS = ["ahWrhrzEAD1", "Hh5bklmdAw7"]

    ATTRIBUTE_IDS = {
        # TEA isLegacyData
        "is_legacy": "b7Lnzn5TPNC",
        # TEA VPD-Epi week onset
        "week_onset": "BJOIp2AWzaD",
        # TEA VPD-Epi year onset
        "year_onset": "MPZ1QsldiKH",
        # TEA VPD-Epi week notification
        "week_notification": "x48FoeDRMV8",
        # TEA VPD-Epi year notification
        "year_notification": "ozzQiwrDfYC"
    }

    def __init__(self):
        dhis2_username, dhis2_password = self.set_credentials()
        self.auth = (dhis2_username, dhis2_password)
        self.session = requests.Session()
        self.session.auth = self.auth
        self.now = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
        self.updated_entities = None
        self.logging_setup()

    def set_credentials(self):
        credentials = {}
        parser = ConfigParser()
        parser.read("/opt/pythonapps/credentials.ini") #CHANGE HERE
        params = parser.items("paho_vpd_prod") #CHANGE HERE

        for param in params:
            credentials[param[0]] = param[1]

        self.SERVER_URL = credentials["server_url"]
        self.RUNTIME_LOG_PATH = credentials["runtime_log_path"]
        self.LOG_FILE = credentials["log_file"]

        return credentials["dhis2_username"], credentials["dhis2_password"] #CHANGE HERE 

    def logging_setup(self):
        # Configure logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[logging.FileHandler(self.LOG_FILE), logging.StreamHandler()]
        )

    def get_epi_date(self, date_str):
        """
        Calculate the correct epidemiological year and week based on WHO rules (Sunday-start week).
        The first epi week of the year is the one containing at least 4 days in the new year.
        """
        # Extract date without time (if format includes "T")
        date_str = date_str.split("T")[0]
        parsed_date = datetime.strptime(date_str, "%Y-%m-%d")

        # Find the first Sunday of the year
        jan1 = datetime(parsed_date.year, 1, 1)
        jan1_weekday = jan1.weekday()  # Monday=0, Sunday=6
        first_sunday = jan1 + timedelta(days=(6 - jan1_weekday) % 7)

        # If the first epi week starts in the previous year (less than 4 days in the new year)
        if (first_sunday - jan1).days >= 4:
            first_sunday -= timedelta(days=7)

        # If date is before the first Sunday, it belongs to last year's last epi week
        if parsed_date < first_sunday:
            return self.get_epi_date(f"{parsed_date.year - 1}-12-31")

        # Compute epi week
        days_since_first_sunday = (parsed_date - first_sunday).days
        epi_week = (days_since_first_sunday // 7) + 1
        epi_year = parsed_date.year

        # Check if the date belongs to the next year's first epi week
        next_year_jan1 = datetime(parsed_date.year + 1, 1, 1)
        next_year_first_sunday = next_year_jan1 + timedelta(days=(6 - next_year_jan1.weekday()) % 7)

        # If next year's first epi week starts in the current year
        if (next_year_first_sunday - next_year_jan1).days >= 4 and parsed_date >= next_year_first_sunday:
            epi_week = 1
            epi_year = parsed_date.year + 1

        # Years with only 52 weeks
        if epi_week == 53:
            # Check if the year actually has a 53rd epi week
            if not self.has_53_weeks(epi_year):
                epi_week = 1
                epi_year += 1

        return str(epi_year), str(epi_week)

    def has_53_weeks(self, year):
        """Check if a given year has 53 epidemiological weeks."""

        # Find the first Sunday of the year
        jan1 = datetime(year, 1, 1)
        first_sunday = jan1 + timedelta(days=(6 - jan1.weekday()) % 7)

        # Find the first Sunday of the next year
        next_year_jan1 = datetime(year + 1, 1, 1)
        next_year_first_sunday = next_year_jan1 + timedelta(days=(6 - next_year_jan1.weekday()) % 7)

        # A year has 53 weeks if it starts on a Sunday OR ends on a Thursday
        return jan1.weekday() == 6 or next_year_first_sunday.day <= 4

    def handle_last_execution(self, program_id, mode='read'):
        """
        Handles reading or writing the last execution timestamp for a program.

        :param program_id: The ID of the DHIS2 program
        :param mode: 'read' to get the timestamp, 'write' to save it
        :return: Timestamp string when reading; None when writing
        """
        log_file = os.path.join(self.RUNTIME_LOG_PATH, f'{program_id}_runtime.log')

        if mode == 'read':
            if os.path.exists(log_file):
                with open(log_file, 'r') as f:
                    return f.read().strip()
            return self.now

        elif mode == 'write':
            with open(log_file, 'w') as f:
                f.write(self.now)

    def fetch_enrollments(self, program_id, page):
        """
        Get all enrollments that were created/updated since last time script execution.
        """
        logging.info(f"Fetching enrollments for program {program_id}, page {page}.")
        url = (f"{self.SERVER_URL}tracker/enrollments.json?fields=trackedEntity&ouMode=ALL"
               f"&pageSize={self.PAGE_SIZE}&page={page}&program={program_id}"
               f"&updatedAfter={self.handle_last_execution(program_id)}")

        response = self.session.get(url)

        if response.status_code != 200:
            logging.error(f"Failed to fetch enrollments: {response.text}")
            return []

        data = response.json().get('instances', [])
        return [entry['trackedEntity'] for entry in data]

    def fetch_tracked_entities(self, program_id, enrollments, page):
        """
        Get all TEI corresponding to enrollments that were created/updated since last time script execution.
        """
        if not enrollments:
            return []

        logging.info(f"Fetching tracked entities for program {program_id}, page {page}.")
        url = (f"{self.SERVER_URL}tracker/trackedEntities.json?fields=orgUnit,trackedEntityType,"
               f"trackedEntity,updatedAt,attributes,enrollments[enrolledAt,occurredAt]"
               f"&ouMode=ALL&pageSize={self.PAGE_SIZE}&program={program_id}"
               f"&trackedEntity={';'.join(enrollments)}")

        response = self.session.get(url)

        if response.status_code != 200:
            logging.error(f"Failed to fetch tracked entities: {response.text}")
            return []

        return response.json().get('instances', [])

    def update_tracked_entities(self, tracked_entities, batch_size=50):
        if not tracked_entities:
            return

        total_entities = len(tracked_entities)
        logging.info(f"Updating tracked entities. Total Count: {total_entities}")

        for i in range(0, total_entities, batch_size):
            batch = tracked_entities[i:i + batch_size]  # Get batch of 50 entities
            payload = {"trackedEntities": batch}

            logging.info(f"Sending batch {i // batch_size + 1}: {len(batch)} entities")

            response = self.session.post(
                f"{self.SERVER_URL}tracker",
                json=payload,
                headers={"Accept": "application/json", "Content-Type": "application/json"},
                params={"async": "false", "mergeMode": "MERGE", "importStrategy": "CREATE_AND_UPDATE"}
            )

            if response.status_code == 200:
                logging.info(f"Batch {i // batch_size + 1} updated successfully.")
                time.sleep(5)  # Wait 5 seconds
                self.updated_entities += len(batch)
            else:
                logging.error(f"Error updating batch {i // batch_size + 1}: {response.text}")

        logging.info(f"Total entities updated: {self.updated_entities}")

    def process_entities(self, program_id):
        # logging.info(f"Processing entities for program {program_id}.")
        page = 1
        while True:
            enrollments = self.fetch_enrollments(program_id, page)
            if not enrollments:
                self.handle_last_execution(program_id, mode='write')
                break

            tracked_entities = self.fetch_tracked_entities(program_id, enrollments, page)
            update_list = []

            for entity in tracked_entities:
                # if isLegacyData continue
                if any(attr['attribute'] == self.ATTRIBUTE_IDS['is_legacy'] for attr in entity['attributes']):
                    continue

                enrollment = entity['enrollments'][0]
                year_onset, week_onset = self.get_epi_date(enrollment['enrolledAt'])
                year_notification, week_notification = self.get_epi_date(enrollment['occurredAt'])

                # For onset att we use enrollment_date = enrolledAt
                # For notif att we use incident_date = occurredAt
                entity['attributes'] = [
                    {"attribute": self.ATTRIBUTE_IDS['week_onset'], "value": week_onset},
                    {"attribute": self.ATTRIBUTE_IDS['year_onset'], "value": year_onset},
                    {"attribute": self.ATTRIBUTE_IDS['week_notification'], "value": week_notification},
                    {"attribute": self.ATTRIBUTE_IDS['year_notification'], "value": year_notification}
                ]

                del entity['enrollments']
                update_list.append(entity)

            if update_list:
                self.update_tracked_entities(update_list)

            page += 1

    def run(self):
        # logging.info("Starting DHIS2 update process.")
        for program_id in self.PROGRAM_IDS:
            self.updated_entities = 0
            self.process_entities(program_id)
            logging.info(f"Processed entities {self.updated_entities} for program {program_id}.")
        # logging.info("DHIS2 update process completed.")


if __name__ == "__main__":
    updater = DHIS2Updater()
    updater.run()
