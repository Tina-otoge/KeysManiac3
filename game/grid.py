class Grid:
    """Manages a responsive 2D grid system"""

    def __init__(self, window, columns_count, rows_count, **create_kwargs):
        self.columns_count = columns_count
        self.rows_count = rows_count
        self.window = window
        self.items = []
        self.create_kwargs = create_kwargs
        self.update()

    def update(self):
        self.cell_width = self.window.width // self.columns_count
        self.cell_height = self.window.height // self.rows_count
        for item in self.items:
            item.update()

    def x(self, x):
        return x * self.cell_width

    def y(self, y):
        return y * self.cell_height

    def add(self, drawable, x, y, width, height):
        self.items.append(self.Item(drawable, x, y, width, height, grid=self))

    def remove(self, drawable):
        for item in self.items:
            if item.drawable is not drawable:
                continue
            self.items.remove(item)
            del item
            break

    class Item:
        def __init__(self, drawable, x, y, width, height, grid):
            self.grid = grid
            self._x = x
            self._y = y
            self._width = width
            self._height = height

            if isinstance(drawable, type):
                drawable = drawable(
                    x=self.x,
                    y=self.y,
                    width=self.width,
                    height=self.height,
                    **self.grid.create_kwargs,
                )
            self.drawable = drawable

        def update(self):
            self.drawable.x = self.x
            self.drawable.y = self.y
            self.drawable.width = self.width
            self.drawable.height = self.height

        @property
        def x(self):
            return self.grid.x(self._x)

        @property
        def y(self):
            return self.grid.y(self._y)

        @property
        def width(self):
            return self.grid.cell_width * self._width

        @property
        def height(self):
            return self.grid.cell_height * self._height
