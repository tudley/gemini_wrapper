class ToDoService:
    def __init__(self):
        self.list = []

    def add_item_to_list(self, item):
        if item in self.list:
            return {
                "status": "fail",
                "text": f"list already contains item: {item}"
            }
        self.list.append(item)
        return {
            "status": "success",
            "text": f"item {item} successfully added to list"
        }

    def add_to_list(items: list[str]):
        for item in items:
            self.add_item_to_list(item)
