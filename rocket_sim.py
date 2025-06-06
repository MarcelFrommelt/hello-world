import math

# 2-stage rocket ascent trajectory simulation
# Generic but realistic parameters

def simulate():
    # Constants
    g = 9.81  # gravitational acceleration (m/s^2)
    rho = 1.225  # air density at sea level (kg/m^3)
    Cd = 0.5  # drag coefficient (typical for rockets)
    A = 1.0  # reference area (m^2)

    # Stage parameters
    stage1 = {
        'dry_mass': 1500.0,   # kg
        'prop_mass': 20000.0, # kg
        'thrust': 3.5e5,      # N
        'burn_time': 120.0    # s
    }

    stage2 = {
        'dry_mass': 500.0,    # kg
        'prop_mass': 5000.0,  # kg
        'thrust': 8e4,        # N
        'burn_time': 100.0    # s
    }

    payload_mass = 1000.0  # kg

    # Initial state
    t = 0.0
    dt = 0.1  # simulation time step
    altitude = 0.0
    velocity = 0.0

    # Setup stage burn times and remaining propellant
    stage = 1
    burn_time_remaining = stage1['burn_time']
    prop_mass_remaining = stage1['prop_mass']

    # Current mass = dry_mass + propellant + remaining stages + payload
    mass = stage1['dry_mass'] + stage1['prop_mass'] + stage2['dry_mass'] + stage2['prop_mass'] + payload_mass

    history = []

    while True:
        # Determine thrust and propellant burn rate
        thrust = 0.0
        burn_rate = 0.0
        if stage == 1 and burn_time_remaining > 0:
            thrust = stage1['thrust']
            burn_rate = stage1['prop_mass'] / stage1['burn_time']
        elif stage == 2 and burn_time_remaining > 0:
            thrust = stage2['thrust']
            burn_rate = stage2['prop_mass'] / stage2['burn_time']

        # Burn propellant
        if burn_time_remaining > 0:
            dm = burn_rate * dt
            if dm > prop_mass_remaining:
                dm = prop_mass_remaining
            prop_mass_remaining -= dm
            mass -= dm
            burn_time_remaining -= dt

            if prop_mass_remaining <= 0:
                burn_time_remaining = 0

        # Stage separation
        if stage == 1 and burn_time_remaining <= 0 and prop_mass_remaining <= 0:
            # drop stage 1 dry mass
            mass -= stage1['dry_mass']
            stage = 2
            burn_time_remaining = stage2['burn_time']
            prop_mass_remaining = stage2['prop_mass']
            continue

        # Compute forces
        weight = mass * g
        drag = 0.5 * Cd * rho * velocity**2 * A
        if velocity < 0:
            drag *= -1  # drag opposes motion

        net_force = thrust - weight - drag
        acceleration = net_force / mass

        # Update state
        velocity += acceleration * dt
        altitude += velocity * dt
        t += dt

        history.append((t, altitude, velocity, mass))

        # Stop if rocket starts descending past launch altitude
        if altitude < 0 and t > 10:
            break

        if stage == 2 and burn_time_remaining <= 0 and altitude > 100000 and velocity <= 0:
            break

        if t > 1000:  # safety stop
            break

    return history


def main():
    history = simulate()
    for t, alt, vel, mass in history:
        if int(t*10) % 50 == 0:  # print every 5 seconds
            print(f"t={t:6.1f} s alt={alt:8.1f} m vel={vel:7.1f} m/s mass={mass:8.1f} kg")


if __name__ == '__main__':
    main()
