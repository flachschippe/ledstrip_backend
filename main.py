from configuration import injector
from ledstrip_service import LedstripService

if __name__ == "__main__":
    ledstrip_service = injector.get(LedstripService)

    ledstrip_service.run()