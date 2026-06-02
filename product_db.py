import sqlite3
from typing import List, Tuple, Optional

class ProductDatabase:
    """SQLite를 사용한 제품 데이터베이스 관리 클래스"""
    
    def __init__(self, db_name: str = "products.db"):
        """데이터베이스 연결 초기화"""
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()
    
    def create_table(self):
        """Products 테이블 생성"""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Products (
                productID INTEGER PRIMARY KEY AUTOINCREMENT,
                productName TEXT NOT NULL,
                productPrice INTEGER NOT NULL
            )
        ''')
        self.conn.commit()
        print("Products 테이블이 생성되었습니다.")
    
    def insert_product(self, product_name: str, product_price: int) -> bool:
        """제품 입력 (CREATE)"""
        try:
            self.cursor.execute('''
                INSERT INTO Products (productName, productPrice)
                VALUES (?, ?)
            ''', (product_name, product_price))
            self.conn.commit()
            print(f"✓ 제품 '{product_name}'이(가) 입력되었습니다. (가격: {product_price}원)")
            return True
        except sqlite3.Error as e:
            print(f"✗ 입력 오류: {e}")
            return False
    
    def get_product(self, product_id: int) -> Optional[Tuple]:
        """특정 제품 검색 (READ - Single)"""
        try:
            self.cursor.execute('''
                SELECT * FROM Products WHERE productID = ?
            ''', (product_id,))
            product = self.cursor.fetchone()
            if product:
                return product
            else:
                print(f"✗ ID {product_id}인 제품을 찾을 수 없습니다.")
                return None
        except sqlite3.Error as e:
            print(f"✗ 검색 오류: {e}")
            return None
    
    def get_all_products(self) -> List[Tuple]:
        """모든 제품 검색 (READ - All)"""
        try:
            self.cursor.execute('SELECT * FROM Products')
            products = self.cursor.fetchall()
            return products
        except sqlite3.Error as e:
            print(f"✗ 검색 오류: {e}")
            return []
    
    def search_by_name(self, product_name: str) -> List[Tuple]:
        """제품명으로 검색 (READ - By Name)"""
        try:
            self.cursor.execute('''
                SELECT * FROM Products WHERE productName LIKE ?
            ''', (f"%{product_name}%",))
            products = self.cursor.fetchall()
            return products
        except sqlite3.Error as e:
            print(f"✗ 검색 오류: {e}")
            return []
    
    def update_product(self, product_id: int, product_name: str = None, 
                      product_price: int = None) -> bool:
        """제품 수정 (UPDATE)"""
        try:
            if product_name and product_price:
                self.cursor.execute('''
                    UPDATE Products 
                    SET productName = ?, productPrice = ?
                    WHERE productID = ?
                ''', (product_name, product_price, product_id))
            elif product_name:
                self.cursor.execute('''
                    UPDATE Products 
                    SET productName = ?
                    WHERE productID = ?
                ''', (product_name, product_id))
            elif product_price:
                self.cursor.execute('''
                    UPDATE Products 
                    SET productPrice = ?
                    WHERE productID = ?
                ''', (product_price, product_id))
            else:
                print("✗ 수정할 데이터가 없습니다.")
                return False
            
            self.conn.commit()
            print(f"✓ ID {product_id}인 제품이 수정되었습니다.")
            return True
        except sqlite3.Error as e:
            print(f"✗ 수정 오류: {e}")
            return False
    
    def delete_product(self, product_id: int) -> bool:
        """제품 삭제 (DELETE)"""
        try:
            self.cursor.execute('DELETE FROM Products WHERE productID = ?', 
                              (product_id,))
            self.conn.commit()
            print(f"✓ ID {product_id}인 제품이 삭제되었습니다.")
            return True
        except sqlite3.Error as e:
            print(f"✗ 삭제 오류: {e}")
            return False
    
    def display_all_products(self):
        """모든 제품 출력"""
        products = self.get_all_products()
        if products:
            print("\n=== 전체 제품 목록 ===")
            print(f"{'ID':<5} {'상품명':<20} {'가격':<10}")
            print("-" * 35)
            for product in products:
                print(f"{product[0]:<5} {product[1]:<20} {product[2]:<10}원")
            print()
        else:
            print("✗ 제품 데이터가 없습니다.\n")
    
    def close(self):
        """데이터베이스 연결 종료"""
        self.conn.close()
        print("데이터베이스 연결이 종료되었습니다.")


# ============== 사용 예제 ==============
if __name__ == "__main__":
    # 데이터베이스 초기화
    db = ProductDatabase("products.db")
    
    # 1. 제품 입력 (CREATE)
    print("\n### 제품 입력 ###")
    db.insert_product("노트북", 1500000)
    db.insert_product("마우스", 50000)
    db.insert_product("키보드", 80000)
    db.insert_product("모니터", 300000)
    
    # 2. 모든 제품 조회 (READ - All)
    print("\n### 모든 제품 조회 ###")
    db.display_all_products()
    
    # 3. 특정 제품 조회 (READ - By ID)
    print("### 특정 제품 조회 ###")
    product = db.get_product(1)
    if product:
        print(f"ID: {product[0]}, 상품명: {product[1]}, 가격: {product[2]}원")
    
    # 4. 제품명으로 검색 (READ - By Name)
    print("\n### 제품명으로 검색 ###")
    search_results = db.search_by_name("마우스")
    for product in search_results:
        print(f"ID: {product[0]}, 상품명: {product[1]}, 가격: {product[2]}원")
    
    # 5. 제품 수정 (UPDATE)
    print("\n### 제품 수정 ###")
    db.update_product(1, product_price=1600000)
    
    # 6. 수정된 제품 확인
    print("\n### 수정된 전체 제품 목록 ###")
    db.display_all_products()
    
    # 7. 제품 삭제 (DELETE)
    print("### 제품 삭제 ###")
    db.delete_product(4)
    
    # 8. 최종 제품 목록
    print("### 최종 제품 목록 ###")
    db.display_all_products()
    
    # 데이터베이스 연결 종료
    db.close()
