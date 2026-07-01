def hotel_cost(num_nights):
    """Calculates total hotel cost based on a fixed price per night."""
    price_per_night = 1300
    return num_nights * price_per_night

def plane_cost(city_flight):
    city = city_flight.strip().lower()


    if city == "paris":
        return 7500
    elif city == "london":
        return 5600
    elif city == "italy":
        return 10000
    else:
        #Default price if they type a city not explicitly listed
        return 8500


def car_rental(rental_days):
    daily_rate = 400
    return rental_days * daily_rate    


def holiday_cost(num_nights, city_flight, rental_days):
    total_hotel = hotel_cost(num_nights)
    total_flight = plane_cost(city_flight)
    total_car = car_rental( rental_days)

    # Calculate and return total combined cost
    return total_hotel + total_flight + total_car


# --- Main Program Execution ---

print("--- Welcome to the Holiday Cost Calculator ---")
print("Available flight destinations: Paris, London, Italy (or enter 'Other')\n")  

# Get the required user inputs
city_flight = input("Enter the city you will be flying to: ")
num_nights = int(input("Enter the number of nights you will be staying at the hotel: "))
rental_days = int(input("Enter the number of days for which you will be hiring a car: "))

# Calculate costs using the coordinator function
flight_expense = plane_cost(city_flight)
hotel_expense = hotel_cost(num_nights)
car_expense = car_rental(rental_days)
grand_total = holiday_cost(num_nights, city_flight, rental_days)


# Print out all the details
print("\n" + "="*40)
print("         HOLIDAY RECEIPT        ")
print("="*40)
print(f"Destination City  :  {city_flight.title()}")
print(f"Hotel stay        : {num_nights} nights(s)")
print(f"Car Rental        : {rental_days} day(s)")
print("-"*40)
print(f"Flight Cost       : R {flight_expense:,.2f}")
print(f"Hotel Cost        : R {hotel_expense:,.2f}")
print(f"Car Rental Cost   : R {car_expense:,.2f}")
print("-"*40)
print(f"TOTAL HOLIDAY COST: R {grand_total:,.2f}")
print("="*40)
