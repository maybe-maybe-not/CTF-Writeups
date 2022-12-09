# The Blacksmith

### Challenge Description

> In the middle of town lies a huge colosseum, where gladiators battle for the glory of being the town's best. Next to the colosseum, is a digital weapon shop owned by a famous blacksmith who sells some of the finest weapons money can buy. Rumor has it that the shop sells a rare sword that gives you a flag.

> The blacksmith only reserves rare items for his most loyal customers or those who've made a name for themselves in the colosseum. However, this preferential treatment has not gone unnoticed. Most of the gladiators are fed up, and have started to boycott the shop. In response, the blacksmith has started rushing to patch his weapon shop code to phase out the "loyalty system" and his code is now full of hotfixes.

> Can you and Jaga use this opportunity to try and get your hands on the rare sword?

> Access the weapon shop API at: http://host:port

The Blacksmith is a challenge that requires us to interact with a shop through a flask API. This shop has a scrapped loyalty challenge that supposedly prevent's us from gaining loyalty by buying some items. The database for the shop is a simple dictionary, storing the customers and items available for purchase.
```py
Weapon = namedtuple("Weapon", ["name", "price", "loyalty_points"])
RestrictedLoyalty = namedtuple("RestrictedLoyalty", ["fame", "point_history"])

SHOP = {
    "customers": [],
    "inventory": {
        "regular": (
            Weapon("brokensword", 5, 0),
            Weapon("woodensword", 5, 1),
            Weapon("stonesword", 10, 2),
            Weapon("ironsword", 50, 10),
            Weapon("goldsword", 100, 20),
            Weapon("diamondsword", 500, 100),
        ),
        "exclusive": (Weapon("flagsword", 5, 0),),
    },
}
```

We can see the available weapons to buy, the goal of the challenge seems clear, we must somehow buy the flagsword, which costs 5 gold and 0 loyalty points.

First we have to create a new customer through the /customer/new endpoint which gives us a customer_id to use to interact with the other end points
```py
@app.get("/customer/new")
def register():
    if LOYALTY_SYSTEM_ACTIVE:
        customer = Customer(id=uuid4().hex, gold=5, loyalty=Loyalty(1, []))
    else:
        # Ensure loyalty immutable
        customer = Customer(
            id=uuid4().hex, gold=5, loyalty=RestrictedLoyalty(1, [])
        )

    SHOP["customers"].append(customer)

    return {"id": customer.id}
```
It seems like the customer is created with 5 gold, so whats stopping us from buying the flagsword? Well the flagsword seems to be under an "exclusive" category, looking at the customer data class, it seems like we need 1337 loyalty points to be an exclusive customer
```py
@dataclass
class Customer:
    id: str
    gold: int
    loyalty: Loyalty | RestrictedLoyalty

    @property
    def tier(self):
        if (self.loyalty.fame + sum(self.loyalty.point_history)) > 1337:
            return "exclusive"
        return "regular"

    @staticmethod
    def index_from_id(id):
        for idx, customer in enumerate(SHOP["customers"]):
            if customer.id == id:
                return idx
        return None


def weapon_from_name(weapons, name):
    for weapon in weapons:
        if weapon.name == name:
            return weapon
    return None
```

I initially thought we had to find some way to reactivate the loyalty system, and somehow get enough gold to buy a bunch of items to get enough loyalty to become an exclusive customer, so I decided to dig a bit deeper into the /buy endpoint, as it was the only realistic endpoint to have some input vulnerability. The first thing that caught my eye was that we could buy a list of items, I realised I didn't actually know how to supply a list of items into a flask api endpoint so after a bit of searching, I found out that you just had to repeat the same query parameter again in the URL
```py
@app.get("/buy")
def buy_item(customer_id="", items: list[str] | None = Query(default=[])):
    customer_idx = Customer.index_from_id(customer_id)

    if customer_idx is None:
        raise HTTPException(status_code=401)

    if items is None:
        return {"purchased": ""}

    match SHOP["customers"][customer_idx].tier:
        case "regular":
            get_weapon = partial(
                weapon_from_name, SHOP["inventory"]["regular"]
            )
        case "exclusive":
            get_weapon = partial(
                weapon_from_name,
                [
                    *SHOP["inventory"]["regular"],
                    *SHOP["inventory"]["exclusive"],
                ],
            )
        case _:
            raise HTTPException(status_code=500)

    cart = []
    for item in items:
        weapon = get_weapon(item)
        if weapon is None:
            raise HTTPException(status_code=404)
        cart.append(weapon)

    total_price = 0
    point_history = []
    for item in cart:
        if item.price > SHOP["customers"][customer_idx].gold:
            raise HTTPException(status_code=403)
        total_price += item.price
        if item.loyalty_points > 0:
            point_history += [item.loyalty_points]

    try:
        if len(point_history) > 0:
            SHOP["customers"][
                customer_idx
            ].loyalty.point_history += point_history
        if SHOP["customers"][customer_idx].gold < total_price:
            raise HTTPException(status_code=403)
        SHOP["customers"][customer_idx].gold -= total_price
    except:
        raise HTTPException(status_code=403)

    if "flagsword" in [weapon.name for weapon in cart]:
        return {"purchased": FLAG}

    return {"purchased": cart}
```
The /buy endpoint has quite a few lines of code, but it can be broken down into 6 steps:
1. Checks that a customer_id and items parameters have been supplied in the URL
```py
    customer_idx = Customer.index_from_id(customer_id)

    if customer_idx is None:
        raise HTTPException(status_code=401)

    if items is None:
        return {"purchased": ""}
```
2. Gets the list of available weapons based on the tier of the customer, meaning unless we have more than 1337 loyalty points, we don't have access to buy the flagsword
```py
match SHOP["customers"][customer_idx].tier:
        case "regular":
            get_weapon = partial(
                weapon_from_name, SHOP["inventory"]["regular"]
            )
        case "exclusive":
            get_weapon = partial(
                weapon_from_name,
                [
                    *SHOP["inventory"]["regular"],
                    *SHOP["inventory"]["exclusive"],
                ],
            )
        case _:
            raise HTTPException(status_code=500)
```
3. Loops through the list of items we are trying to buy, returning 404 if it does not exist in our available items.
```py
    for item in items:
        weapon = get_weapon(item)
        if weapon is None:
            raise HTTPException(status_code=404)
        cart.append(weapon)
```
4. After validating the list of items, it loops through them again, for each item, it checks that the customer has enough gold to buy only that item, then adds the amount of loyalty points of that item to us.
```py
    total_price = 0
    point_history = []
    for item in cart:
        if item.price > SHOP["customers"][customer_idx].gold:
            raise HTTPException(status_code=403)
        total_price += item.price
        if item.loyalty_points > 0:
            point_history += [item.loyalty_points]
```
5. It checks that we have enough gold to buy all the items that we supplied to the endpoint, if not, it throws a 403 error, if we do have enough, it simply subtracts the total price from our gold.
```py

    try:
        if len(point_history) > 0:
            SHOP["customers"][
                customer_idx
            ].loyalty.point_history += point_history
        if SHOP["customers"][customer_idx].gold < total_price:
            raise HTTPException(status_code=403)
        SHOP["customers"][customer_idx].gold -= total_price
    except:
        raise HTTPException(status_code=403)
```
6. Lastly, if we are buying the flagsword, it gives us the flag, else it just returns the items we have purchased.
```py
    if "flagsword" in [weapon.name for weapon in cart]:
        return {"purchased": FLAG}

    return {"purchased": cart}
```

There are 2 important things of note here. Firstly, the code adds the loyalty point to us before checking that we have enough money to buy all the items supplied. Secondly, it only deducts the total cost of the items if we can actually afford it, meaning if there was an item that gave us loyalty points and only cost at most 5 gold, and we bought a few copies of that item, we will still get loyalty points but have no gold deducted, as the total cost will exceed 5 gold. Luckily for us, the wooden sword fulfils that criteria, costing only 5 gold and giving us 1 loyalty point.

Thus all we have to do is buy more than 1337 wooden swords and we will have enough loyalty points to buy the flag, as we will still have 5 gold, we can simply buy the flag sword afterwards. At first I tried buying 1400 wooden swords at one go but got some error, presumably because the resulting url was too long, so I separated it into 14 requests.
```py
url = <IP> + /buy?customer_id=<customer_id>
payload = url + "&items=woodensword"*100
for i in range(14):
  requests.get(payload)
x = requests.get(url + "&items=flagsword")
print(x.text)
```
Running this gives us the flag `STF22{y0u_b0ught_4_v3ry_3xcLu51v3_sw0rd_w3LL_d0n3_31337}`

I was very surprised that it actually worked and thought I would get some other error, this challenge was quite fun and required a bit of careful reading.
