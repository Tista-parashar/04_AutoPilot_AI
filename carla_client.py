import carla

def main():
    try:
        client = carla.Client("localhost", 2000)
        client.set_timeout(10.0)

        world = client.get_world()

        print("Connected to CARLA!")
        print("Map:", world.get_map().name)

    except Exception as e:
        print("Connection failed:")
        print(e)

if __name__ == "__main__":
    main()