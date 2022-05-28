import time
import diningHallScrapper

if __name__ == '__main__':
    start_time = time.time()

    dhScrapper = diningHallScrapper.diningHallWebScrapper()
    dhScrapper.startDiningHallScrapper()
    dhScrapper.createFoodResultsJson()

    finish_time = time.time()
    print("Runtime:", str((finish_time - start_time) / 60.0), "minutes")
