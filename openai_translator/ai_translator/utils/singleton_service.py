import threading

class SingletonService:
    _instance = None
    _lock = threading.Lock()  # 确保线程安全

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super(SingletonService, cls).__new__(cls)
                    cls._instance.init_service(*args, **kwargs)
        return cls._instance

    def init_service(self, config=None):
        """
        初始化服务的方法，可以在这里设置一些全局配置
        """
        self.config = config
        print("SingletonService initialized with config:", config)

    def get_service_data(self):
        return self.config
