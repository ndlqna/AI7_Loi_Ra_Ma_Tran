# Team AI7 Đức Lên_Tấn Minh_Khánh Minh_Thanh Tiến_Ngọc Khoa #
"""
    Cách chạy chương trình
        mở terminal gõ lệnh
        pip intall pygame
        và chạy chương trình thôi :)
    Toàn bộ code Lên đã chú thích đầy đủ rồi chỉ cần đọc là hiểu
"""
import pygame
import math
# import queue để sử dụng cho thuật toán A* tìm đường đi
from queue import PriorityQueue
import random


WIDTH = 600  # Khung Nhìn
WIN = pygame.display.set_mode((WIDTH, WIDTH)) # Kích Thước cửa sổ khi hiện game
pygame.display.set_caption("Lối Đi Ma Trận") # Tên Khi Hiện Ra Game
# Thiết Lập Màu Sắc 
RED = (252, 255, 21)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (219, 219, 219)
BLACK = (0, 0, 0)
PURPLE = (255,0, 0)
ORANGE = (255, 165 ,0) 
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)
class Node:
    def __init__(self, row, col, width, total_rows):
        #Khởi tạo một Node mới với các thuộc tính cơ bản
        # Vị trí hàng của Node trong lưới
        self.row = row
        # Vị trí cột của Node trong lưới
        self.col = col
        # Tọa độ x của Node trên cửa sổ
        self.x = row * width
        # Tọa độ y của Node trên cửa sổ
        self.y = col * width
        # Màu sắc hiện tại của Node
        self.color = WHITE
        # Danh sách các Node lân cận
        self.neighbors = []
        # Độ rộng của Node
        self.width = width
        # Tổng số hàng trong lưới
        self.total_rows = total_rows
    #Trả về vị trí của Node trong lưới dưới dạng (row, col)
    def get_pos(self):
        return self.row, self.col
    #Kiểm tra xem Node có trong trạng thái 'closed'
    def is_closed(self):
        return self.color == RED
    #Kiểm tra xem Node có trong trạng thái 'open'
    def is_open(self):
        return self.color == GREEN
    # Tương Tự Vậy Thôi Nha AE
    def is_barrier(self):
        return self.color == BLACK

    def is_start(self):
        return self.color == ORANGE

    def is_end(self):
        return self.color == TURQUOISE
    #Đặt Màu của Node về màu trắng
    def reset(self):
        self.color = WHITE

    def make_start(self):
        self.color = ORANGE

    def make_closed(self):
        self.color = RED

    def make_open(self):
        self.color = GREEN

    def make_barrier(self):
        self.color = BLACK

    def make_end(self):
        self.color = TURQUOISE

    def make_path(self):
        self.color = PURPLE
    # Vẽ Node với màu sắc đã được đặt ở trên
    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))
    
    def update_neighbors(self, grid):
        # Cập nhật danh sách các Node lân cận dựa trên lưới đã cho.
        """Hàm này được sử dụng để cập nhật danh sách các Node lân cận của Node hiện tại trong lưới.
        Các Node lân cận được xác định dựa trên vị trí của Node trong lưới và không phải là rào cản.
        Sau khi cập nhật, danh sách neighbors của Node hiện tại sẽ chứa các Node lân cận có thể di chuyển đến.
        Thứ tự xác định các Node lân cận: BOTTOM (dưới), TOP (trên), RIGHT (phải), LEFT (trái)."""
        # Đối tượng Node hiện tại.
        self.neighbors = []
        # DOWN
        """Kiểm tra xem Node hiện tại không nằm ở hàng cuối cùng và Node láng giềng phía dưới 
        không phải là rào cản. Nếu điều kiện này được thỏa mãn, Node láng giềng phía dưới 
        sẽ được thêm vào danh sách Node láng giềng của Node hiện tại"""
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row + 1][self.col])
        # UP
        """Kiểm tra xem Node hiện tại không nằm ở hàng đầu tiên và Node láng giềng phía trên 
        không phải là rào cản. Nếu điều kiện này được thỏa mãn, Node láng giềng phía trên sẽ 
        được thêm vào danh sách Node láng giềng của Node hiện tại."""
        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row - 1][self.col])
        # RIGHT
        """ Kiểm tra xem Node hiện tại không nằm ở cột cuối cùng và Node láng giềng bên phải 
        không phải là rào cản. Nếu điều kiện này được thỏa mãn, Node láng giềng bên phải sẽ
        được thêm vào danh sách Node láng giềng của Node hiện tại."""
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col + 1])
        # LEFT
        """Kiểm tra xem Node hiện tại không nằm ở cột đầu tiên và Node láng giềng bên trái 
        không phải là rào cản. Nếu điều kiện này được thỏa mãn, Node láng giềng bên trái 
        sẽ được thêm vào danh sách Node láng giềng của Node hiện tại."""
        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier(): 
            self.neighbors.append(grid[self.row][self.col - 1])
    # Phương thức so sánh cần thiết cho sắp xếp trong hàng đợi ưu tiên
    def __lt__(self, other):
        return False

def h(p1, p2):
    """
    Hàm tính khoảng cách heuristic giữa hai điểm trong không gian 2D.
    Tham số:
    - p1: Tọa độ điểm đầu (x1, y1).
    - p2: Tọa độ điểm cuối (x2, y2).
    Hàm này tính và trả về khoảng cách heuristic giữa hai điểm p1 và p2.
    Khoảng cách heuristic là tổng độ lớn của sự chênh lệch về giá trị tuyệt đối
    giữa các tọa độ x và y của hai điểm trong không gian 2 chiều.
    """
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)
    
def reconstruct_path(came_from, current, draw):
    """
    Xây dựng đường đi từ đích về điểm bắt đầu theo thuật toán tìm đường.
    Tham số:
    - came_from: Dictionary lưu lại các bước trước của mỗi Node trong quá trình tìm đường.
    - current: Node hiện tại, bắt đầu từ Node đích và di chuyển về phía Node bắt đầu.
    - draw: Hàm vẽ lại cửa sổ để hiển thị quá trình tạo đường đi.
    Hàm này sử dụng thông tin trong dictionary came_from để tái tạo đường đi từ Node đích
    về Node bắt đầu theo thuật toán tìm đường. Khi di chuyển qua mỗi Node trên đường đi,
    nó gọi hàm make_path() để biểu thị Node đó thuộc đường đi, sau đó gọi hàm draw() để vẽ lại cửa sổ.
    """
    while current in came_from:
        # Trong khi vẫn còn Node trong danh sách 'came_from':
        current = came_from[current]  # Di chuyển đến Node trước đó trong đường đi tối ưu
        current.make_path()  # Đánh dấu Node hiện tại là một phần của đường đi tối ưu
        draw()  # Cập nhật giao diện để hiển thị Node hiện tại đã được đánh dấu là một phần của đường đi tối ưu


def algorithm(draw, grid, start, end):
    """Mục đích của hàm algorithm là thực hiện thuật toán A* để tìm đường đi 
    ngắn nhất từ điểm bắt đầu đến điểm kết thúc trong ma trận ô vuông.
    Hàm này sử dụng hàng đợi ưu tiên để duyệt các ô và cập nhật các điểm g
    (độ dài đường đi từ điểm bắt đầu tới ô hiện tại) và điểm f (tổng điểm g và h)
    của từng ô. Khi thuật toán hoàn thành, nếu tìm thấy đường đi từ điểm bắt đầu
    tới điểm kết thúc, nó sẽ trả về True, ngược lại sẽ trả về False.
    Các bước trong thuật toán A* được thực hiện để tìm đường đi ngắn nhất 
    trong ma trận từ điểm bắt đầu tới điểm kết thúc"""
    count = 0
    # Tạo một hàng đợi ưu tiên để lưu trữ các ô đang xét
    open_set = PriorityQueue()
    # Thêm ô bắt đầu vào hàng đợi với độ ưu tiên là 0
    open_set.put((0, count, start))  
    # Dictionary để lưu vị trí trước của mỗi ô
    came_from = {}  
    # Gán điểm g cho mỗi ô trong ma trận là vô cực
    g_score = {node: float("inf") for row in grid for node in row}
    # Điểm g của ô bắt đầu là 0
    g_score[start] = 0  
    # Gán điểm f cho mỗi ô trong ma trận là vô cực
    f_score = {node: float("inf") for row in grid for node in row} 
    # Điểm f của ô bắt đầu được tính dựa trên hàm h()
    f_score[start] = h(start.get_pos(), end.get_pos())
    # Set để lưu trữ các ô đã xét
    open_set_hash = {start}  
    # Vòng lặp chạy cho đến khi hàng đợi không còn phần tử
    while not open_set.empty():  
        # Kiểm tra sự kiện trong Pygame
        for event in pygame.event.get():  
            if event.type == pygame.QUIT:
                pygame.quit()
        # Lấy ô có độ ưu tiên thấp nhất từ hàng đợi
        current = open_set.get()[2]
        # Xóa ô đã lấy ra khỏi set
        open_set_hash.remove(current)  
        # Nếu ô hiện tại là ô kết thúc
        if current == end:  
            # Tái tạo đường đi từ điểm cuối về điểm đầu
            reconstruct_path(came_from, end, draw)  
            # Đánh dấu ô kết thúc
            end.make_end() 
            # Trả về True, đã tìm thấy đường đi 
            return True  
        # Duyệt qua các ô lân cận của ô hiện tại
        for neighbor in current.neighbors:  
            # Tính điểm g tạm thời cho ô lân cận
            temp_g_score = g_score[current] + 1  
            # Nếu điểm g tạm thời nhỏ hơn điểm g hiện tại của ô lân cận
            if temp_g_score < g_score[neighbor]:  
                # Lưu vị trí trước của ô lân cận
                came_from[neighbor] = current  
                # Cập nhật điểm g của ô lân cận
                g_score[neighbor] = temp_g_score 
                # Cập nhật điểm f của ô lân cận
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos()) 
                # Nếu ô lân cận chưa được xét 
                if neighbor not in open_set_hash:  
                    count += 1
                    # Thêm ô lân cận vào hàng đợi với độ ưu tiên f_score
                    open_set.put((f_score[neighbor], count, neighbor))  
                    # Đánh dấu ô lân cận đã xét
                    open_set_hash.add(neighbor) 
                    # Đánh dấu ô lân cận đã xét trên giao diện 
                    neighbor.make_open()  
        # Vẽ lại trạng thái mới sau mỗi vòng lặp
        draw()
         # Nếu ô hiện tại không phải là ô bắt đầu
        if current != start:
            # Đánh dấu ô hiện tại đã xét xong
            current.make_closed()
    # Trả về False nếu không tìm thấy đường đi
    return False


def make_grid(rows, width):
    """
    Tạo lưới chứa các Node dựa trên số hàng và chiều rộng được cung cấp.
    Tham số:
    - rows: Số hàng trong lưới.
    - width: Chiều rộng của lưới.
    Hàm này tạo một lưới bằng cách thêm các Node vào grid dựa trên số hàng và chiều rộng.
    Mỗi Node có vị trí hàng và cột trong lưới, cũng như chiều rộng của nó và tổng số hàng trong lưới.
    Sau đó, hàm này thêm rào cản (barriers) vào một số Node ngẫu nhiên để tạo cấu trúc giống mê cung.
    Các Node được chọn để là rào cản có xác suất ngẫu nhiên (ở đây là 30%).
    Returns:
    - grid: Lưới chứa các Node sau khi đã tạo và thêm rào cản.
    """
    grid = []  # Khởi tạo lưới
    gap = width // rows  # Tính khoảng cách giữa các Node

    # Tạo lưới với các Node và thêm vào grid
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i, j, gap, rows)  # Tạo Node với vị trí và kích thước
            grid[i].append(node)  # Thêm Node vào hàng tương ứng trong grid

    # Thêm rào cản ngẫu nhiên vào một số Node để tạo cấu trúc mê cung
    for row in grid:
        for node in row:
            if random.random() < 0.3:  # Chọn ngẫu nhiên với xác suất 30% (có thể điều chỉnh)
                node.make_barrier()  # Đánh dấu Node là rào cản
    return grid  # Trả về lưới chứa các Node đã tạo và thêm rào cản

def draw_grid(win, rows, width):
    """
    Vẽ lưới trên cửa sổ với kích thước và số hàng cụ thể.
    Tham số:
    - win: Cửa sổ Pygame để vẽ lưới.
    - rows: Số hàng trong lưới.
    - width: Chiều rộng của lưới.
    Hàm này vẽ lưới trên cửa sổ Pygame với kích thước và số hàng cụ thể.
    Nó sử dụng Pygame để vẽ các đường kẻ theo chiều dọc và ngang để tạo thành lưới.
    Mỗi đường kẻ được vẽ từ điểm (0, i * gap) đến (width, i * gap) (chiều ngang),
    và từ điểm (j * gap, 0) đến (j * gap, width) (chiều dọc).
    Tham số gap tính toán khoảng cách giữa các đường kẻ để tạo lưới.
    Returns:
    Không trả về giá trị, chỉ vẽ lưới lên cửa sổ Pygame đã được chỉ định.
    """
    gap = width // rows  # Tính khoảng cách giữa các đường kẻ
    for i in range(rows):
        # Vẽ đường kẻ ngang từ (0, i * gap) đến (width, i * gap)
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
        for j in range(rows):
            # Vẽ đường kẻ dọc từ (j * gap, 0) đến (j * gap, width)
            pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))

def draw(win, grid, rows, width):
    """
    Vẽ lưới các Node và lưới (grid) trên cửa sổ Pygame.
    Tham số:
    - win: Cửa sổ Pygame để vẽ lưới.
    - grid: Lưới chứa các Node.
    - rows: Số hàng trong lưới.
    - width: Chiều rộng của lưới.
    Hàm này làm các bước sau để vẽ lưới trên cửa sổ Pygame:
    1. Fill cửa sổ với màu trắng (WHITE).
    2. Vẽ từng Node trong lưới:
       - Duyệt qua mỗi hàng trong lưới.
       - Với mỗi Node trong hàng, gọi phương thức draw() của Node để vẽ Node đó lên cửa sổ.
    3. Vẽ lưới (grid) bằng cách sử dụng hàm draw_grid() đã được định nghĩa trước đó.
    4. Cập nhật cửa sổ Pygame để hiển thị các thay đổi vừa được vẽ.
    Returns:
    Không trả về giá trị, chỉ vẽ lưới lên cửa sổ Pygame đã được chỉ định.
    """
    win.fill(WHITE)  # Fill cửa sổ với màu trắng
    # Vẽ từng Node trong lưới
    for row in grid:
        for node in row:
            node.draw(win)  # Vẽ Node lên cửa sổ Pygame
    draw_grid(win, rows, width)  # Vẽ lưới (grid)
    pygame.display.update()  # Cập nhật cửa sổ để hiển thị các thay đổi


def get_clicked_pos(pos, rows, width):
    """
    Chuyển đổi vị trí chuột trên cửa sổ Pygame thành vị trí hàng và cột trong lưới.

    Tham số:
    - pos: Vị trí chuột trên cửa sổ Pygame (x, y).
    - rows: Số hàng trong lưới.
    - width: Chiều rộng của lưới.
    Hàm này nhận vị trí chuột trên cửa sổ Pygame và chuyển đổi nó thành vị trí hàng và cột
    tương ứng trong lưới dựa trên số hàng và chiều rộng của lưới.
    Returns:
    - row: Vị trí hàng trong lưới dựa trên vị trí chuột.
    - col: Vị trí cột trong lưới dựa trên vị trí chuột.
    """
    gap = width // rows  # Tính khoảng cách giữa các Node
    y, x = pos  # Lấy tọa độ chuột (x, y)
    row = y // gap  # Tính vị trí hàng dựa trên vị trí chuột
    col = x // gap  # Tính vị trí cột dựa trên vị trí chuột
    return row, col  # Trả về vị trí hàng và cột trong lưới dựa trên vị trí chuột


def main(win, width):
    """
    Hàm chính thực thi chương trình để tạo cửa sổ Pygame và xử lý các sự kiện.
    Tham số:
    - win: Cửa sổ Pygame để vẽ lên.
    - width: Chiều rộng của cửa sổ.
    Hàm này tạo cửa sổ Pygame và bắt đầu vòng lặp chính để xử lý các sự kiện.
    Trong vòng lặp này:
    - Vẽ lưới và các Node lên cửa sổ.
    - Xử lý các sự kiện chuột và bàn phím:
        - Click chuột trái để đặt điểm bắt đầu, điểm kết thúc và rào cản.
        - Click chuột phải để xóa các điểm đã đặt.
        - Ấn phím SPACE để thực hiện thuật toán tìm đường từ điểm bắt đầu đến điểm kết thúc.
        - Ấn phím 'c' để xóa các điểm bắt đầu và kết thúc cũ, và tạo một lưới mới.
    - Khi thuật toán tìm đường được thực hiện (SPACE được ấn), nó sẽ gọi thuật toán algorithm() để thực hiện tìm đường.
    Returns:
    Không trả về giá trị, chỉ chạy chương trình và xử lý các sự kiện trên cửa sổ Pygame.
    """
    ROWS = 60  # Số hàng trong lưới
    grid = make_grid(ROWS, width)  # Tạo lưới
    start = None  # Node bắt đầu
    end = None  # Node kết thúc
    run = True
    while run:
        draw(win, grid, ROWS, width)  # Vẽ lưới và các Node lên cửa sổ Pygame
        for event in pygame.event.get():  # Lặp qua các sự kiện
            if event.type == pygame.QUIT:
                run = False  # Thoát vòng lặp khi nhấn nút thoát

            if pygame.mouse.get_pressed()[0]:  # Click chuột trái
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                node = grid[row][col]
                if not start and node != end :
                    start = node
                    start.make_start()  # Đánh dấu Node là điểm bắt đầu

                elif not end and node != start:
                    end = node
                    end.make_end()  # Đánh dấu Node là điểm kết thúc

                elif node != end and node != start:
                    node.make_barrier()  # Đánh dấu Node là rào cản

            elif pygame.mouse.get_pressed()[2]:  # Click chuột phải
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                node = grid[row][col]
                node.reset()  # Reset Node về trạng thái mặc định
                if node == start:
                    start = None
                elif node == end:
                    end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    # Cập nhật các Node lân cận cho từng Node trong lưới
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)

                    # Thực hiện thuật toán tìm đường
                    algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)
                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)  # Tạo lưới mới

    pygame.quit()  # Kết thúc chương trình Pygame khi thoát


main(WIN, WIDTH)
# Tạm Biệt Hihi  
