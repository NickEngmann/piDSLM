# Design Improvements for piDSLM

This directory contains design improvement documentation and 3D model exports for the piDSLM project.

## Overview

The piDSLM enclosure has been improved with better modularity, heat management, and printability. This document outlines the design improvements.

## Design Files

- **PiDSLR.fzz**: Original FreeCAD design file
- **PiDSLR_v2.fzz**: Updated design with improvements (see below)
- **STL Export**: 3D printable files in `stl/` directory
- **STEP Export**: CAD exchange format in `step/` directory

## Design Improvements (v2)

### 1. Modular Camera Grips

The enclosure now supports interchangeable grips:
- **Standard Grip**: Vertical orientation for handheld use
- **Horizontal Grip**: Landscape orientation support
- **Tripod Mount**: Standard 1/4"-20 threaded hole

### 2. Heat Management

Improved ventilation for extended operation:
- Rear ventilation slots (5mm gaps)
- Bottom heat sink fins
- Camera module clearance for airflow

### 3. Cable Management

- Internal cable channels
- Side cable exit ports
- strain relief features

### 4. Printability

- Optimized part orientations
- Reduced support material requirements
- Wall thickness optimized for FDM printing (2.4mm)

### 5. Assembly Improvements

- Magnetic camera module mount
- Screwless panel retention
- Snap-fit bezel design

## CAD Software

- **OnShape**: Cloud-based collaborative design
  - View interactive model: https://bit.ly/raspi-onshape
  
- **FreeCAD**: Open-source CAD (for local modifications)
  - Export to STL: File → Export → Select "STL" format

## 3D Printing

### Recommended Settings

- **Material**: PLA, PETG, or ABS
- **Layer Height**: 0.2mm (0.15mm for better finish)
- **Infill**: 20% for structural parts
- **Wall Thickness**: 2.4mm (12mm perimeter at 0.2mm layer)
- **Supports**: Minimal with optimized orientations

### Print Parts

1. Main enclosure body (1x)
2. Top cover (1x)
3. Side panel (1x)
4. Camera grip module (2x - optional)
5. Tripod mount adapter (1x - optional)

## Bill of Materials

### Hardware
- Raspberry Pi 3/4 (or 2)
- HQ Camera Module
- MHS35-TFT Display
- 4x M3x12mm screws
- 2x M3 nuts (for tripod mount)
- 2x Neodymium magnets (Ø10mm, 3mm thick)

### Optional
- 18650 battery pack (2x)
- Battery holder
- USB-C power module

## Version History

### v2.0 (Current)
- Modular grip design
- Improved heat management
- Cable management channels
- Magnetic camera mount
- Optimized for 3D printing

### v1.0 (Original)
- Basic enclosure
- Fixed grip design
- Limited ventilation

## Contributing Design Improvements

We welcome design contributions! To submit improvements:

1. Fork the repository
2. Export your design changes from OnShape or FreeCAD
3. Add new STL files to `stl/` directory
4. Update this README with your changes
5. Submit a pull request

Please include:
- Description of the improvement
- Parts list (if any new components)
- Print settings recommendations
- Compatibility notes

## License

This design is released under the Creative Commons Attribution-ShareAlike 4.0 International License. You are free to share and adapt the design, provided you:
- Give appropriate credit
- Share your modifications under the same license
