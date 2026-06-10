#!/usr/bin/env python3

class CashRegister:
  """
  CashRegister represents a simple point-of-sale register.

  Attributes:
    discount (int): percentage discount applied to the total (0-100).
    total (float): current total amount in the register.
    items (list): list of item titles added (duplicates for multiple quantities).
    previous_transactions (list): history of transactions; each entry is a dict
      with keys: 'title', 'price', 'quantity', 'amount'.
  """

  def __init__(self, discount=0):
    """
    Initialize a CashRegister.

    Args:
      discount (int, optional): percentage discount to apply. Defaults to 0.

    Validation:
      - `discount` must be an integer between 0 and 100 inclusive.
      - If invalid, prints "Not valid discount" and sets discount to 0.
    """
    self.total = 0
    # validate discount: must be integer between 0 and 100 inclusive
    if not isinstance(discount, int) or discount < 0 or discount > 100:
      print("Not valid discount")
      self.discount = 0
    else:
      self.discount = discount

    # list of item titles (repeated for multiple quantities)
    self.items = []

    # keep a history of previous transactions (each is a dict with title, price, quantity, amount)
    # used for voiding and for operations that need transaction context
    self.previous_transactions = []

    # track last transaction amount (legacy support for earlier behavior)
    self.last_transaction = 0

  def add_item(self, title, price, quantity=1):
    """
    Add an item to the register.

    - Increases `total` by `price * quantity`.
    - Appends `title` into `items` `quantity` times.
    - Records a transaction dict into `previous_transactions`.
    """
    amount = price * quantity
    self.total += amount

    # add the item title once per quantity to the items list
    for _ in range(quantity):
      self.items.append(title)

    self.last_transaction = amount

    # record the transaction for future operations (e.g., voiding)
    self.previous_transactions.append({
      'title': title,
      'price': price,
      'quantity': quantity,
      'amount': amount
    })

  def apply_discount(self):
    """
    Apply the configured percentage discount to the current `total`.

    Behavior:
      - If there are no `previous_transactions`, prints
        "There is no discount to apply." and returns.
      - Otherwise, reduces `total` by `discount` percent and prints a message
        with the updated total (rounded to int if whole number).
      - After applying the discount, removes the last transaction record from
        `previous_transactions` and removes the corresponding item titles from
        `items` (preserving other items). This follows the specified requirement
        to remove the last item of `previous_transactions` when discount is applied.
    """
    if not self.previous_transactions:
      print("There is no discount to apply.")
      return

    # apply discount to the current total if set
    if self.discount:
      self.total = self.total * (100 - self.discount) / 100
      try:
        if float(self.total).is_integer():
          print(f"After the discount, the total comes to ${int(self.total)}.")
        else:
          print(f"After the discount, the total comes to ${self.total}.")
      except Exception:
        print(f"After the discount, the total comes to ${self.total}.")
    else:
      print("There is no discount to apply.")

    # remove the last transaction record and its items from `items`
    if self.previous_transactions:
      last = self.previous_transactions.pop()
      qty = last.get('quantity', 1)
      title = last.get('title')
      for _ in range(qty):
        for i in range(len(self.items)-1, -1, -1):
          if self.items[i] == title:
            self.items.pop(i)
            break

  def void_last_transaction(self):
    """
    Void (remove) the last recorded transaction.

    - Pops the last transaction from `previous_transactions`.
    - Subtracts its `amount` from `total`.
    - Removes the corresponding item titles from the end of `items`.
    - Ensures `total` does not go below 0.
    """
    if not self.previous_transactions:
      return

    last = self.previous_transactions.pop()
    self.total -= last.get('amount', 0)

    # remove the last N items matching the title from the end
    qty = last.get('quantity', 1)
    title = last.get('title')
    for _ in range(qty):
      # only remove if present
      for i in range(len(self.items)-1, -1, -1):
        if self.items[i] == title:
          self.items.pop(i)
          break

    if self.total < 0:
      self.total = 0.0
