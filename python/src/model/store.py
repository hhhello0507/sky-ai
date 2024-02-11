class Store:
    def __init__(self, class_names):
        self.class_names = class_names
        self.predict_store = [0 for _ in range(len(class_names))]

    def get_max_index(self) -> int:
        return [*sorted([i for i in enumerate(self.predict_store)], key=lambda x: x[1])][0][0]

    def init_predict_store(self):
        self.predict_store = [0 for _ in range(len(self.class_names))]