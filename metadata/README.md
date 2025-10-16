# VPD-SMART Metadata Package Installation Guide

## Overview

VPD-SMART (Vaccine-Preventable Disease Surveillance, Monitoring, Analysis, Reporting, and Training) provides PAHO-approved DHIS2 metadata packages for disease surveillance. This guide covers the installation process for VPD-SMART metadata packages.

## Available Packages

- **Acute Flaccid Paralysis (AFP)** - Complete surveillance package with case investigation forms, laboratory tracking, and reporting dashboards
- **Measles & Rubella (MR)** - Integrated surveillance system with outbreak investigation tools and vaccination tracking

## Prerequisites

- DHIS2 version 2.39 or higher
- System administrator privileges
- Minimum server requirements: 16GB RAM, 4 CPU cores
- Backup of your current DHIS2 instance (recommended)

## Importing a Metadata File into DHIS2

### Step 1: Prepare the Metadata File

1. Download the VPD-SMART metadata package from the [GitHub repository](https://github.com/IM-Data-PAHO/vpd-smart/tree/main/metadata)
2. Extract the downloaded ZIP file to access the JSON metadata files
3. Review the package documentation for any country-specific customizations needed

### Step 2: Access the Import/Export App

1. Login to your DHIS2 instance with administrator privileges
2. Navigate to **Apps** → **Import/Export**
3. Select the **Metadata Import** option from the left sidebar

### Step 3: Configure Import Settings

Before importing, configure the following settings:

#### Import Strategy
- **Identifier**: Select "UID" (recommended for VPD-SMART packages)
- **Import Report Mode**: Choose "ERRORS" to see only critical issues
- **Preheat Cache**: Enable this option for better performance
- **Import Strategy**: Select "CREATE_AND_UPDATE" to allow both new objects and updates

#### Advanced Options
- **Atomic Mode**: Select "ALL" for complete import or rollback
- **Merge Mode**: Choose "REPLACE" for clean installation
- **Flush Mode**: Select "AUTO" for optimal performance
- **Skip Sharing**: Leave unchecked to maintain proper access controls
- **Skip Validation**: Leave unchecked for data integrity
- **Async**: Enable for large packages to prevent timeout

### Step 4: Upload and Import

1. Click **Choose File** and select your VPD-SMART JSON metadata file
2. Review the import settings one final time
3. Click **Import** to begin the process
4. Monitor the import progress - this typically takes 5-15 minutes depending on package size

### Step 5: Verify Import Results

After import completion:

1. **Review Import Summary**: Check for any errors or warnings in the import report
2. **Verify Data Elements**: Navigate to **Maintenance** → **Data Element** to confirm VPD-SMART elements are present
3. **Check Programs**: Go to **Programs** to verify tracker programs (AFP/MR case investigations)
4. **Validate Dashboards**: Access **Apps** → **Dashboard** to see VPD-SMART analytics dashboards
5. **Test Data Entry**: Try entering test data using the **Capture** app

## Post-Installation Configuration

### Essential Configuration Steps

1. **Organization Unit Assignment**
   - Assign VPD-SMART programs to relevant organization units
   - Configure data capture locations

2. **User Access Configuration**
   - Create user roles for VPD surveillance staff
   - Assign appropriate sharing permissions
   - Configure capture access for data entry users

3. **Data Validation Rules**
   - Review and activate validation rules
   - Configure validation notifications

4. **Indicator Configuration**
   - Verify indicator calculations
   - Configure dashboard analytics

### Optional Enhancements

1. **GIS Integration**
   - Import geographical boundaries for spatial analysis
   - Configure map visualizations

2. **Custom Widgets**
   - Install VPD-SMART custom widgets (epi-week, line-listing, vpd-tools)
   - Configure dashboard integrations

3. **SMS Integration**
   - Configure SMS gateway for mobile data collection
   - Set up SMS notifications

## Troubleshooting Common Issues

### Import Errors

**Error**: "Object with identifier 'XXX' already exists"
- **Solution**: Use "CREATE_AND_UPDATE" import strategy or clean conflicting objects

**Error**: "Validation failed for object"
- **Solution**: Check object dependencies and ensure all required metadata is present

**Error**: "Import timeout"
- **Solution**: Enable "Async" mode or import in smaller chunks

### Post-Import Issues

**Missing Dashboards**
- Verify dashboard sharing settings
- Check user access permissions

**Data Entry Forms Not Visible**
- Confirm program assignment to organization units
- Verify user capture permissions

**Indicators Not Calculating**
- Check data element mappings
- Verify organization unit levels in indicators

## Support and Documentation

- **Technical Support**: [Request support](mailto:vpd-support@paho.org)
- **Documentation**: [DHIS2 Import/Export Guide](https://docs.dhis2.org/en/use/user-guides/dhis-core-version-master/maintaining-the-system/importexport-app.html)
- **Community Forum**: Join our community discussions
- **GitHub Issues**: [Report bugs or request features](https://github.com/IM-Data-PAHO/vpd-smart/issues)

## Additional Resources

- [PAHO VPD Surveillance Guidelines](https://www.paho.org/en/topics/immunization)
- [DHIS2 Metadata Management Best Practices](https://docs.dhis2.org/en/implement/managing-dhis2-data/metadata.html)
- [VPD-SMART Training Materials](https://academy.dhis2.org/courses/)

---

**Note**: This installation guide is based on DHIS2 2.40+. For older versions, some interface elements may differ slightly. Always backup your system before importing metadata packages.

For country-specific customizations or advanced configuration needs, please contact the PAHO VPD-SMART technical team for assistance.