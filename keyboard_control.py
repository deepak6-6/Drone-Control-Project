import asyncio
from mavsdk import System
from mavsdk.offboard import VelocityBodyYawspeed

async def run():
    drone = System()
    await drone.connect(system_address="udp://:14540")

    print("Waiting for drone...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print("Connected!")
            break

    await drone.action.arm()
    await drone.action.takeoff()
    await asyncio.sleep(5)

    print("Starting offboard mode...")

    await drone.offboard.set_velocity_body(
        VelocityBodyYawspeed(0.0, 0.0, 0.0, 0.0)
    )

    try:
        await drone.offboard.start()
    except Exception as e:
        print(f"Offboard start failed: {e}")
        return

    print("Controls: w/s/a/d/q/e, x = land")

    while True:
        key = input("Enter command: ")

        if key == "w":
            await drone.offboard.set_velocity_body(
                VelocityBodyYawspeed(1.0, 0.0, 0.0, 0.0))
        elif key == "s":
            await drone.offboard.set_velocity_body(
                VelocityBodyYawspeed(-1.0, 0.0, 0.0, 0.0))
        elif key == "a":
            await drone.offboard.set_velocity_body(
                VelocityBodyYawspeed(0.0, -1.0, 0.0, 0.0))
        elif key == "d":
            await drone.offboard.set_velocity_body(
                VelocityBodyYawspeed(0.0, 1.0, 0.0, 0.0))
        elif key == "q":
            await drone.offboard.set_velocity_body(
                VelocityBodyYawspeed(0.0, 0.0, -1.0, 0.0))
        elif key == "e":
            await drone.offboard.set_velocity_body(
                VelocityBodyYawspeed(0.0, 0.0, 1.0, 0.0))
        elif key == "x":
            await drone.action.land()
            break

asyncio.run(run())
