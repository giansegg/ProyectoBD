from Firma import Firma
import time

if __name__ == "__main__":
    start_time = time.time()

    firma: Firma = Firma(1000)
    firma.createData()

    elapsed_time = time.time() - start_time

    print(f"Execution time: {elapsed_time} seconds")


