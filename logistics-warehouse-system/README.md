# Σύστημα Διαχείρισης Αποθηκών

Comprehensive warehouse management system built with Flask and MongoDB.

## Features

- **Role-based Access Control**: Admin, Supervisor, Employee roles
- **Inventory Management**: Track products, quantities, sales
- **Real-time Analytics**: Profit/loss tracking, volume usage
- **Transaction History**: Complete audit trail
- **Docker Deployment**: Easy containerized deployment

## Quick Start

### Prerequisites
- Docker Desktop installed
- Git (for cloning)

### Installation & Running

1. **Clone the repository:**
```bash
git clone https://github.com/your-username/logistics-warehouse-system.git
cd logistics-warehouse-system
```

2. **Start the application:**
```bash
docker compose up -d --build
```

3. **Access the application:**
- Open your browser and go to: `http://localhost:5000`

4. **Login with default admin account:**
- Username: `admin`
- Password: `admin123`

### Stopping the application:
```bash
docker compose down
```

## User Roles & Access

### Admin (Διαχειριστής)
- **Login**: username: `admin`, password: `admin123`
- **Capabilities**: 
  - Create/manage warehouses
  - Create/manage products
  - Create/manage supervisors
  - View company-wide statistics
  - Access any warehouse as supervisor

### Supervisor (Προϊστάμενος)
- **Login**: Created by Admin with format `name.surname.unitid`
- **Capabilities**:
  - All employee functions
  - Create/manage employees
  - Purchase products
  - View unit statistics
  - Change employee passwords

### Employee (Υπάλληλος)
- **Login**: Created by Supervisor with format `name.surname.unitid`
- **Capabilities**:
  - View products in their warehouse
  - Search and filter products
  - Sell products
  - View product details
  - Change their own password

## Project Structure

```
logistics-warehouse-system/
├── app/
│   ├── templates/          # HTML templates
│   ├── static/            # CSS, JS, images
│   ├── __init__.py        # App initialization
│   ├── main.py           # Main Flask application
│   ├── database.py       # MongoDB connection
│   ├── models.py         # Database models
│   ├── admin_routes.py   # Admin functionality
│   ├── supervisor_routes.py # Supervisor functionality
│   └── employee_routes.py   # Employee functionality
├── data/                  # MongoDB data volume
├── Dockerfile            # Docker image definition
├── compose.yaml          # Docker compose configuration
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## Database Schema

The system uses MongoDB with the following collections:
- `users`: User accounts (admin, supervisors, employees)
- `units`: Warehouse information
- `products_master`: Global product catalog
- `unit_products`: Product quantities per warehouse
- `transactions`: Sales/purchase history

## API Endpoints

### Authentication
- `GET /`: Landing page
- `POST /login`: User authentication
- `GET /logout`: User logout

### Admin Routes (`/admin/`)
- `GET /admin/`: Admin dashboard
- `GET|POST /admin/create_unit`: Create warehouse
- `GET|POST /admin/create_product`: Create product
- `GET|POST /admin/create_supervisor`: Create supervisor
- `GET /admin/units`: View warehouses
- `GET /admin/supervisors`: View supervisors

### Supervisor Routes (`/supervisor/`)
- `GET /supervisor/`: Supervisor dashboard
- `GET|POST /supervisor/create_employee`: Create employee
- `GET /supervisor/employees`: Manage employees
- `GET /supervisor/statistics`: Unit statistics
- `POST /supervisor/purchase_product/<id>`: Purchase products

### Employee Routes (`/employee/`)
- `GET /employee/`: Employee dashboard
- `GET /employee/products`: View products with search/filter
- `GET /employee/product/<id>`: Product details
- `POST /employee/sell_product/<id>`: Sell products

## Configuration

Environment variables (in `.env`):
- `MONGODB_URI`: MongoDB connection string
- `SECRET_KEY`: Flask secret key
- `FLASK_ENV`: Environment (development/production)

## Development

To run in development mode:

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Set environment variables:**
```bash
export MONGODB_URI="mongodb://localhost:27017/LogisticsDB"
export FLASK_ENV=development
```

3. **Run Flask app:**
```bash
cd app
python main.py
```

## Docker Configuration

- **Flask App**: Runs on port 5000
- **MongoDB**: Runs on port 27017
- **Data Persistence**: MongoDB data stored in `./data` volume
- **Networks**: Both containers on same Docker network

## Troubleshooting

1. **Port conflicts**: If port 5000 or 27017 are in use, modify `compose.yaml`
2. **Permission issues**: Ensure Docker has access to the project directory
3. **Database issues**: Check MongoDB logs with `docker compose logs mongo`
4. **App issues**: Check Flask logs with `docker compose logs web`

## License

This project is part of an academic assignment for Information Systems coursework.