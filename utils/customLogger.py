import logging

class logGeneration:
    @staticmethod
    def logGenerate():
        logging.basicConfig(filename=".\\Logs.\\APITestExecution.log", format='%(asctime)s: %(levelname)s: %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)
        return logger