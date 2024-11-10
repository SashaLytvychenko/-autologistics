========================
Autologistics Management
========================

This Odoo module provides a comprehensive system for managing car logistics, from receiving vehicles to handling repairs and maintaining records of dealer and driver information. The module is designed to streamline the process of car inventory management, service history tracking, and repair workflows within a logistics operation.

Features
========

The Autologistics Management module offers the following key functionalities:

### 1. Car Receiving and Tracking
- **VIN Management**: Records each vehicle's VIN code, ensuring uniqueness to prevent duplicate entries.
- **Dealership and Driver Tracking**: Associates each car with a specific dealer and truck driver.
- **Expected and Actual Arrival Dates**: Allows users to track when a car is expected in stock and when it actually arrives.

### 2. Vehicle Status Management
- **Status Updates**: Supports various status options for each vehicle, including:
  - `Draft`: Initial status when a car is registered.
  - `In Stock`: Car is available in the logistics stock.
  - `Awaiting Decision`: Car is pending further instructions.
  - `Repair`: Car is in the process of being repaired.
  - `Sent to Dealer`: Car has been sent to the dealer.
  - `Cancelled`: The record is cancelled and no longer active.

### 3. Detailed Car Information
- **Brand and Model Details**: Records brand, body type, and other specifications, such as engine type, transmission, and fuel capacity.
- **Additional Features**: Tracks extra features like seat heating, steering wheel heating, cruise control, rearview camera, and parking sensors.
- **Service Book Availability**: Indicates whether a car comes with a service book.

### 4. Repair Management
- **Repair Records**: Allows users to create detailed repair records, including services performed, repair start and end dates, and additional repair notes.
- **Service Price Calculation**: Calculates the total cost of repairs based on services performed on the car.
- **Priority Levels**: Assigns priorities to repair jobs, aiding in workflow organization.
- **Integration with Services**: Links to predefined repair services, such as bumper or door repair, and calculates total service costs automatically.

### 5. Chatter Integration
- **Automated Chatter Messages**: Posts updates in the Odoo Chatter system, particularly for significant status changes (e.g., when a car is sent to a dealer).

### 6. Security and Access Control
- **Deletion Restriction**: Prevents the deletion of records unless the car is in the `Draft` status, maintaining data integrity.

Dependencies
============
This module depends on the following modules:
- `mail` (for chatter and notifications)
- `base` (for core functionalities)


Technical Details
=================
- **Model Structure**: This module includes the following main models:
  - `autolog.receive.car`: Manages receiving and tracking information of cars.
  - `autolog.repair.car`: Manages repair details and services for each car.
  - `autolog.car.dealer`, `autolog.truck.driver`: Stores dealer and driver details.

- **Views**: Provides form and tree views for car and repair management, making data entry straightforward.

- **Actions and Wizards**: Includes custom wizards to simplify status updates and streamline the workflow for car repairs.


