import pandas as pd
import os

# File paths
train_file_path = "data/trains.csv"
passenger_file_path = "data/passengers.csv"

# Load train data from CSV


def load_train_data(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File {file_path} not found.")
    data = pd.read_csv(file_path)
    # Convert columns to appropriate data types
    data["Total Seats"] = pd.to_numeric(data["Total Seats"], errors='coerce')
    data["Available Seats"] = pd.to_numeric(
        data["Available Seats"], errors='coerce')
    data["Total Fare"] = pd.to_numeric(data["Total Fare"], errors='coerce')
    return data

# Load passenger data from CSV


def load_passenger_data(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File {file_path} not found.")
    data = pd.read_csv(file_path)
    # Convert columns to appropriate data types
    data["Number of tickets"] = pd.to_numeric(
        data["Number of tickets"], errors='coerce')
    return data

# Check seat availability


def check_seat_availability(train_data, train_id, num_tickets):
    train = train_data[train_data["Train ID"] == train_id]
    if train.empty:
        raise ValueError("Invalid Train ID")
    available_seats = train.iloc[0]["Available Seats"]
    return available_seats >= num_tickets

# Update seat availability


def update_seat_availability(train_data, train_id, num_tickets):
    train_data.loc[train_data["Train ID"] ==
                   train_id, "Available Seats"] -= num_tickets

# Generate report showing train details


def generate_train_report(train_data):
    report = train_data[["Train Name", "Source Station",
                         "Destination Station", "Available Seats"]]
    report.to_csv("train_report.csv", index=False)
    print("Train report generated: train_report.csv")

# Generate report showing total revenue from each train


def generate_revenue_report(train_data, confirmed_bookings):
    revenue = {}
    for booking in confirmed_bookings:
        train_id = booking["Train ID"]
        num_tickets = booking["Number of tickets"]
        fare = train_data.loc[train_data["Train ID"]
                              == train_id, "Total Fare"].values[0]
        total_fare = fare * num_tickets
        if train_id in revenue:
            revenue[train_id] += total_fare
        else:
            revenue[train_id] = total_fare

    revenue_df = pd.DataFrame(list(revenue.items()), columns=[
                              "Train ID", "Total Revenue"])
    revenue_df.to_csv("revenue_report.csv", index=False)
    print("Revenue report generated: revenue_report.csv")

# Main function


def main():
    try:
        train_data = load_train_data(train_file_path)
        passenger_data = load_passenger_data(passenger_file_path)

        confirmed_bookings = []

        for _, row in passenger_data.iterrows():
            passenger_name = row["Passenger Name"]
            train_id = row["Train ID"]
            num_tickets = row["Number of tickets"]

            if check_seat_availability(train_data, train_id, num_tickets):
                update_seat_availability(train_data, train_id, num_tickets)
                confirmed_bookings.append(row)
                print(
                    f"Booking confirmed for {passenger_name} on train {train_id}.")
            else:
                print(
                    f"Insufficient seats for {passenger_name} on train {train_id}.")

        generate_train_report(train_data)
        generate_revenue_report(train_data, confirmed_bookings)

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
