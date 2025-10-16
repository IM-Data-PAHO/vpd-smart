# VPD-SMART Geographical Maps

This directory contains official geographical boundary files for countries implementing VPD-SMART surveillance packages. These maps enable accurate spatial analysis and visualization of disease surveillance data in DHIS2.

## Overview

To enhance the analytical capabilities of VPD-SMART, accurate and granular geographical boundaries for administrative divisions were integrated. These boundaries were sourced from official national sources and validated in collaboration with national counterparts to ensure their quality and relevance for spatial analysis within the system.

## File Structure

Each country folder contains three administrative levels in GML format:

```
[COUNTRY_CODE]/
├── [COUNTRY]_ADM0_GML.gml          # Level 0 - Country boundaries
├── [COUNTRY]_ADM0_GML.qmd          # Level 0 - Metadata
├── [COUNTRY]_ADM0_GML.xsd          # Level 0 - Schema definition
├── [COUNTRY]_ADM1_GML_2025.gml     # Level 1 - Regional boundaries
├── [COUNTRY]_ADM1_GML_2025.qmd     # Level 1 - Metadata
├── [COUNTRY]_ADM1_GML_2025.xsd     # Level 1 - Schema definition
├── [COUNTRY]_ADM2_GML_2025.gml     # Level 2 - District boundaries
├── [COUNTRY]_ADM2_GML_2025.qmd     # Level 2 - Metadata
└── [COUNTRY]_ADM2_GML_2025.xsd     # Level 2 - Schema definition
```

## Administrative Levels

- **Level 0 (ADM0)**: Country boundaries
- **Level 1 (ADM1)**: Regional/State/Province boundaries  
- **Level 2 (ADM2)**: District/Municipality boundaries

## Available Countries

- **PRY**: Paraguay

## File Formats

### GML Files (.gml)
Geography Markup Language files containing the actual boundary coordinates and geographical features. These files are directly importable into DHIS2 for spatial analysis.

### QMD Files (.qmd)
Quarto markdown files containing metadata and documentation about the geographical boundaries, including data sources, validation processes, and usage guidelines.

### XSD Files (.xsd)
XML Schema Definition files that define the structure and validation rules for the corresponding GML files.

## Integration with DHIS2

These geographical boundaries integrate seamlessly with VPD-SMART packages through:

1. **GIS_CODE Integration**: Each boundary includes PAHO-created GIS codes for consistent identification
2. **DHIS2 Compatibility**: Files are formatted for direct import into DHIS2 instances
3. **Spatial Analysis**: Enables advanced spatial analysis and visualization of VPD surveillance data

## Usage

1. Select the appropriate country folder
2. Import the GML files into your DHIS2 instance following the [installation guide](https://im-data-paho.github.io/vpd-smart)
3. Configure organizational units to match the geographical boundaries
4. Enable spatial analysis features in your VPD-SMART dashboards

## Data Sources and Validation

All geographical boundaries are:
- Sourced from official national mapping agencies
- Validated in collaboration with national health ministry counterparts
- Updated regularly to reflect administrative changes
- Quality-assured for spatial analysis accuracy

## Support and Documentation

For technical support and detailed documentation:
- Visit: [https://im-data-paho.github.io/vpd-smart](https://im-data-paho.github.io/vpd-smart)
- Contact: VPD-SMART Technical Team
- GitHub: [https://github.com/IM-Data-PAHO/vpd-smart](https://github.com/IM-Data-PAHO/vpd-smart)

## License

These geographical boundary files are provided under the same license as VPD-SMART packages. Please refer to the main repository for licensing terms.

---

**Note**: This spatial analysis capacity is crucial for informing targeted public health interventions and policies, and for facilitating spatially oriented research on VPD distribution and determinants, thereby directly impacting the system's utility for policy and research.