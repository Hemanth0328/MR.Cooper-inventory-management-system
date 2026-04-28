from abc import ABC, abstractmethod
from collections import deque
from datetime import datetime

class Product(ABC):
    def __init__(self, sku, name, price, qty):
        self.sku, self.name, self.price, self.qty = sku, name, price, qty
    @abstractmethod
    def cat(self): pass

class Elec(Product):
    def cat(self): return "Electronics"
class Groc(Product):
    def cat(self): return "Grocery"
class Cloth(Product):
    def cat(self): return "Clothing"
class Warehouse:
    _i = None
    def __new__(cls):
        if not cls._i:
            cls._i = super().__new__(cls)
            cls._i.products = {}
            cls._i.grns = []
            cls._i.logs = []
            cls._i.stack = []
            cls._i.queue = deque()
        return cls._i
    def scan(self, sku):
        p = self.products.get(sku)
        if p:
            print(f"{p.sku} | {p.name} | {p.cat()} | Qty:{p.qty}")
        else:
            print("Product SKU not recognized")

    def receive(self, sku, qty, sup):
        p = self.products.get(sku)
        if not p: return print("Not found")
        self.stack.append((sku, p.qty))
        p.qty += qty
        self.grns.append(f"GRN | {sku} | +{qty} | {sup} | {datetime.now():%d-%m %H:%M}")
        self.logs.append(f"IN | {sku} | +{qty}")
        print(f"{p.name}: now {p.qty}")

    def dashboard(self):
        for p in self.products.values():
            print(f"{p.sku} | {p.name} | {p.cat()} | Rs.{p.price} | Qty:{p.qty} {'LOW!' if p.qty<=5 else ''}")

    def alerts(self):
        for p in self.products.values():
            if p.qty <= 5: print(f"LOW: {p.name} Qty:{p.qty}")

    def create_po(self, sku, qty, sup):
        self.queue.append((sku, qty, sup))
        self.logs.append(f"PO | {sku} | {qty}")
        print(f"PO queued: {sku} x{qty}")

    def fulfil(self):
        if not self.queue: return print("No POs")
        sku, qty, sup = self.queue.popleft()
        p = self.products.get(sku)
        if p:
            p.qty += qty
            self.grns.append(f"GRN | {sku} | +{qty} | {sup} | {datetime.now():%d-%m %H:%M}")
            self.logs.append(f"IN | {sku} | +{qty}")
            print(f"Done: {p.name} +{qty}")

    def undo(self):
        if not self.stack: return print("Nothing")
        sku, old = self.stack.pop()
        p = self.products.get(sku)
        if p: p.qty = old; print(f"Undo: {p.name} -> {old}")

w = Warehouse()
w.products = {"S1":Elec("S1","Laptop",45000,10), "S2":Groc("S2","Rice",450,3), "S3":Cloth("S3","Shirt",599,2)}

while True:
    print("\n1.Scan 2.Receive 3.GRN 4.Dashboard 5.Alerts 6.PO 7.Fulfil 8.Logs 9.Undo 0.Exit")
    c = input("> ")
    if   c=='1': w.scan(input("SKU: ").upper())
    elif c=='2': w.receive(input("SKU: ").upper(), int(input("Qty: ")), input("Supplier: "))
    elif c=='3': [print(g) for g in w.grns] if w.grns else print("None")
    elif c=='4': w.dashboard()
    elif c=='5': w.alerts()
    elif c=='6': w.create_po(input("SKU: ").upper(), int(input("Qty: ")), input("Supplier: "))
    elif c=='7': w.fulfil()
    elif c=='8': [print(l) for l in w.logs] if w.logs else print("None")
    elif c=='9': w.undo()
    elif c=='0': break


