import pandas as pd
import matplotlib.pyplot as plt


# ============ CLASSES ============

class Vehicle:
    def __init__(self, vehicle_id, name, vehicle_type, fuel_type, capacity):
        self.vehicle_id = vehicle_id
        self.name = name
        self.vehicle_type = vehicle_type
        self.fuel_type = fuel_type
        self.capacity = capacity
        self.status = "Available"
        self.total_km = 0
        self.fuel_used = 0


class Driver:
    def __init__(self, driver_id, name, license_no, experience_years):
        self.driver_id = driver_id
        self.name = name
        self.license_no = license_no
        self.experience_years = experience_years
        self.assigned_vehicle = None


class Trip:
    def __init__(self, trip_id, vehicle_id, driver_id, start_location, end_location, distance_km, fuel_consumed, date):
        self.trip_id = trip_id
        self.vehicle_id = vehicle_id
        self.driver_id = driver_id
        self.start_location = start_location
        self.end_location = end_location
        self.distance_km = distance_km
        self.fuel_consumed = fuel_consumed
        self.date = date

    def fuel_efficiency(self):
        if self.fuel_consumed > 0:
            return round(self.distance_km / self.fuel_consumed, 2)
        return 0


# ============ FLEET MANAGER ============

class FleetManager:
    def __init__(self):
        self.vehicles = {}
        self.drivers = {}
        self.trips = []

    def add_vehicle(self, vehicle):
        self.vehicles[vehicle.vehicle_id] = vehicle
        print(f"Vehicle {vehicle.vehicle_id} added successfully.")

    def add_driver(self, driver):
        self.drivers[driver.driver_id] = driver
        print(f"Driver {driver.driver_id} added successfully.")

    def assign_driver(self, driver_id, vehicle_id):
        if driver_id in self.drivers and vehicle_id in self.vehicles:
            self.drivers[driver_id].assigned_vehicle = vehicle_id
            self.vehicles[vehicle_id].status = "On Trip"
            print(f"Driver {driver_id} assigned to vehicle {vehicle_id}.")
        else:
            print("Invalid driver or vehicle ID.")

    def log_trip(self, trip):
        self.trips.append(trip)
        if trip.vehicle_id in self.vehicles:
            v = self.vehicles[trip.vehicle_id]
            v.total_km += trip.distance_km
            v.fuel_used += trip.fuel_consumed
            v.status = "Available"
        print(f"Trip {trip.trip_id} logged successfully.")

    def fleet_summary(self):
        data = []
        for v in self.vehicles.values():
            avg_efficiency = round(v.total_km / v.fuel_used, 2) if v.fuel_used > 0 else 0
            data.append({
                "Vehicle ID": v.vehicle_id,
                "Name": v.name,
                "Type": v.vehicle_type,
                "Status": v.status,
                "Total KM": v.total_km,
                "Fuel Used": v.fuel_used,
                "Avg Efficiency (km/l)": avg_efficiency
            })
        return pd.DataFrame(data)

    def trip_summary(self):
        data = []
        for t in self.trips:
            data.append({
                "Trip ID": t.trip_id,
                "Vehicle ID": t.vehicle_id,
                "Driver ID": t.driver_id,
                "Route": f"{t.start_location} -> {t.end_location}",
                "Distance (km)": t.distance_km,
                "Fuel Consumed (L)": t.fuel_consumed,
                "Efficiency (km/l)": t.fuel_efficiency(),
                "Date": t.date
            })
        return pd.DataFrame(data)

    def most_used_vehicle(self):
        df = self.fleet_summary()
        if df.empty:
            return "No data available"
        return df.loc[df['Total KM'].idxmax()]

    def least_efficient_vehicle(self):
        df = self.fleet_summary()
        df = df[df['Avg Efficiency (km/l)'] > 0]
        if df.empty:
            return "No data available"
        return df.loc[df['Avg Efficiency (km/l)'].idxmin()]


# ============ MAIN PROGRAM ============

if __name__ == "__main__":

    fleet = FleetManager()

    # Add Vehicles
    fleet.add_vehicle(Vehicle("V001", "Tata Ace", "Truck", "Diesel", 1000))
    fleet.add_vehicle(Vehicle("V002", "Maruti Van", "Van", "Petrol", 500))
    fleet.add_vehicle(Vehicle("V003", "Ashok Leyland", "Truck", "Diesel", 2000))
    fleet.add_vehicle(Vehicle("V004", "Tata Nexon EV", "Car", "EV", 5))

    # Add Drivers
    fleet.add_driver(Driver("D001", "Ramesh Kumar", "KA01-12345", 5))
    fleet.add_driver(Driver("D002", "Suresh Babu", "KA02-67890", 3))
    fleet.add_driver(Driver("D003", "Lakshmi Devi", "KA03-54321", 7))

    # Assign Drivers
    fleet.assign_driver("D001", "V001")
    fleet.assign_driver("D002", "V002")
    fleet.assign_driver("D003", "V003")

    # Log Trips
    fleet.log_trip(Trip("T001", "V001", "D001", "Bangalore", "Mysore", 150, 15, "2026-06-10"))
    fleet.log_trip(Trip("T002", "V002", "D002", "Bangalore", "Chennai", 350, 28, "2026-06-11"))
    fleet.log_trip(Trip("T003", "V003", "D003", "Bangalore", "Hyderabad", 570, 60, "2026-06-12"))
    fleet.log_trip(Trip("T004", "V001", "D001", "Bangalore", "Coimbatore", 365, 35, "2026-06-13"))
    fleet.log_trip(Trip("T005", "V004", "D002", "Bangalore", "Tumkur", 70, 10, "2026-06-14"))

    # Reports
    print("\n=== FLEET SUMMARY ===")
    df_fleet = fleet.fleet_summary()
    print(df_fleet)

    print("\n=== TRIP SUMMARY ===")
    df_trips = fleet.trip_summary()
    print(df_trips)

    print("\n=== MOST USED VEHICLE ===")
    print(fleet.most_used_vehicle())

    print("\n=== LEAST EFFICIENT VEHICLE ===")
    print(fleet.least_efficient_vehicle())

    # Save to CSV
    df_fleet.to_csv('fleet_summary.csv', index=False)
    df_trips.to_csv('trip_summary.csv', index=False)
    print("\nCSV files saved: fleet_summary.csv, trip_summary.csv")

    # Charts
    df_fleet.plot(x='Name', y='Total KM', kind='bar', figsize=(8, 5), color='steelblue', legend=False)
    plt.title('Total Distance Covered by Each Vehicle')
    plt.ylabel('Kilometers')
    plt.xticks(rotation=30)
    plt.tight_layout()
    plt.savefig('total_km_by_vehicle.png')
    plt.show()

    df_eff = df_fleet[df_fleet['Avg Efficiency (km/l)'] > 0]
    df_eff.plot(x='Name', y='Avg Efficiency (km/l)', kind='bar', figsize=(8, 5), color='green', legend=False)
    plt.title('Fuel Efficiency by Vehicle (km/l)')
    plt.ylabel('km per Liter')
    plt.xticks(rotation=30)
    plt.tight_layout()
    plt.savefig('fuel_efficiency.png')
    plt.show()

    df_trips.plot(x='Trip ID', y='Distance (km)', kind='bar', figsize=(8, 5), color='orange', legend=False)
    plt.title('Trip Distances')
    plt.ylabel('Distance (km)')
    plt.tight_layout()
    plt.savefig('trip_distances.png')
    plt.show()

print("\nCharts saved: total_km_by_vehicle.png, fuel_efficiency.png, trip_distances.png")