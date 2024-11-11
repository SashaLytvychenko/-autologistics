.. _changelog:

Changelog
=========

`17.0.1.0.0`
----------------
### Added
- Added tests to verify core module functionality.
- Added `uk_UA` translation.
- Included demo data and tests to showcase module features.
- Added an ``index.html`` file with a module description.

### Structure
- Created complete module structure with essential files and dependencies.

### Features
- Implemented `AutologisticCar` model to manage the intake and tracking of cars in inventory, including VIN, status, locations, and car attributes.
- Enforced unique VIN constraint and restricted record deletion to 'draft' status only.
- Added actions for updating car statuses and creating repair records.
- Integrated automatic status change to "in stock" with arrival date setting.

### Improvements
- Optimized model field structure and annotations for improved readability and user support.