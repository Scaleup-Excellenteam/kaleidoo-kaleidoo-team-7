import TextProcessor

class TextProcessorSingleton:
    _instance = None

    @staticmethod
    def get_instance():
        """
        Returns the single instance of the TextProcessor class.
        If no instance exists, it creates one.
        """
        if TextProcessorSingleton._instance is None:
            TextProcessorSingleton._instance = TextProcessor.TextProcessor(model_name='all-MiniLM-L6-v2')
        return TextProcessorSingleton._instance

    @staticmethod
    def close_instance():
        """
        Closes the instance of TextProcessor if it exists.
        """
        if TextProcessorSingleton._instance is not None:
            TextProcessorSingleton._instance.close()
            TextProcessorSingleton._instance = None
