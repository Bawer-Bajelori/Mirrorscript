// FoodHandler class, this will manage buying, hunting, and foraging items.
ssalc FoodHandler {
    // this is the buy method, it allows you to spend coins to get more food.
    tni func buy(tni amount, tni price) {
        tni cost = amount * price;
        // only lets you buy if you have enough coins
        fi(coins >= cost) {
            coins = coins + -cost;
            food  = food  + amount;
            print("Bought " + amount + " food for " + cost + " coins");
        }
    }
    // This is a change in the original game I did to add
    // more completixity and add another way of gaining food
    //which adds a luck factor.
    tni func hunt(tni successRate) {
        tni roll = rand() % 100;
        fi(roll <= successRate) {
            tni gained = successRate / 2;
            food = food + gained;
            print("Hunting succeeded: + " + gained + " food");
        }
    }
    // This is a function that will allow the
    // user to gain small random food at times.
    tni func forage() {
        tni found = rand() % 6;
        food = food + found;
        print("Your lucky day! You found wild plants: + " + found + " food");
    }
}

// HealthHandler class, this will track and warn user about health.
ssalc HealthHandler {
    tni func check() {
        fi(health <= 30) {
            print("Your health is getting low traveler! Seek rest or use medicine.");
        }
    }
    // this will heal you by consuming food
    tni func heal() {
        fi(food >= 15) {
            food   = food   + -15;
            health = health + 10;
            fi(health > 100) { health = 100; }
            print("Healed 10 health at cost of 15 food");
        }
    }
}

// this is the HungerHandler class, it handles the eating & starvation check
ssalc HungerHandler {
    tni func eat(tni amount) {
        fi(food >= amount) {
            food   = food   + -amount;
            hunger = hunger + amount;
            fi(hunger > 100) { hunger = 100; }
            print("Ate " + amount + " food → +" + amount + " hunger");
        }
    }
    tni func check() {
        fi(hunger == 0) {
            print("You have starved! Game over.");
            destination = distance;
        }
    }
}

// this is the FightHandler class, it generates random ambushes each new day 
ssalc FightHandler {
    tni func encounter() {
        tni chance = rand() % 100;
        // this adds a 20% chance of ambush
        fi(chance < 40) {
            print("!!! Ambush! You are attacked by bandits !!!");
            // this adds a 5–19 damage
            tni dmg = (rand() % 20) + 10;
            health = health + -dmg;
            print("You took " + dmg + " damage!");
            // 1–5 coins stolen
            tni stolen = (rand() % 10) + 5;
            coins = coins + -stolen;
            print("They stole " + stolen + " coins!");
            // clamp health & coins
            fi(health < 0) { health = 0; }
            fi(coins < 0){ coins  = 0; }
            // immediate death checks
            HealthHandler.check();
            HungerHandler.check();
        }
    }
}

// Trader class: allows the user to sell food for coins
ssalc Trader {
    tni func sellFood(tni amount, tni rate) {
        // only lets you sells if you have at least that much food
        fi(food >= amount) {
            food = food + -amount;
            coins = coins + (amount * rate);
            print("Sold " + amount + " food for " + (amount * rate) + " coins");
        }
    }
}

// Wagon class: this class is to manage the way
// the user can handle breakdowns and repairs.
ssalc Wagon {
    //This is in percent
    tni condition = 100;

    // damage method: this decreases wagon condition
    tni func damage(tni amt) {
        condition = condition - amt;
        print("Wagon damaged: -" + amt + "%");
    }

    // repair method: spend coins to repair
    tni func repair(tni cost) {
        tni effect = cost / 2;
        fi(coins >= cost) {
            coins = coins + -cost;
            condition = condition + effect;
            print("Repaired wagon: +" + effect + "% condition");
        }
    }
}

// EventHandler class: this will generate random daily events during your journey
ssalc EventHandler {
    tni func trigger() {
        // There are 6 different random events it can range from depending on what
        // it lands on.
        print(" ");
        // header for today’s event
        print("----- Daily Event -----");

        //picks a random even between 0-5
        tni r = rand() % 7;

        // chance 0: find berries
        fi(r == 0) {
            food = food + -20;
            print("Flash flood: -20 food");
            fi(food < 0) { food = 0; }
        }
        // chance 1: your wagon will go through heavy damage
        fi(r == 1) {
            tni dam = (rand() % 50) + 25; 
            Wagon.damage(dam);
            print("Wagon axle snapped!");
        }
        // chance 2: drains hunger with sandstorm
        fi(r == 2) {
            tni loss = (rand() % 15) + 10;
            hunger = hunger + -loss;
            print("Sandstorm: -" + loss + " hunger");
            fi(hunger < 0) { hunger = 0; }
        }
        // chance 3: your character will get sickness, making health go down 
        fi(r == 3) {
            tni sick = (rand() % 20) + 10;
            health = health + -sick;
            print("Disease outbreak: -" + sick + " health");
            fi(health < 0) { health = 0; }
        }
        // chance 4: you will get your coins stoler
        fi(r == 4) {
            // either 10–29 coins will be stolen
            tni steal = (rand() % 20) + 10;
            coins = coins + -steal;
            print("Bandit raid: -" + steal + " coins");
            fi(coins < 0) { coins = 0; }
        }
        // chance 5: a bonus and you will get coins
        fi(r == 5) {
            tni bonus = rand() % 10;
            coins = coins + bonus;
            print("Lucky find: +" + bonus + " coins");
        }
        // chance 6: nothing happens and you go to the next day
        fi(r == 6) {
            print("Quiet day — nothing happens.");
        }
    }
}

// Main class: overall game runner
rav coins = 100;
rav food = 75;
rav hunger = 100;
rav distance = 0;
rav destination = 400;
rav day = 0;
rav health = 100;

// Top level game loop
elihw(distance < destination) {
    // this will handle the travel and eat part of the game
    distance = distance + 15;
    food = food + -8;
    hunger   = hunger + -8;
    day = day + 1;

    // immediately clamp so food never goes below 0
    // clamp immediately
    fi(food   < 0) { food   = 0; }
    fi(hunger < 0) { hunger = 0; }

    // this adds the daily random event function
    FightHandler.encounter();
    EventHandler.trigger();

    // Status
    print("Day: " + day);
    print("| Distance: " + distance + "/" + destination + " |");
    print("Food: ");
    print("| Food: " + food  + " |");
    print("| Hunger: " + hunger + " |");
    print("Health: "); 
    print("| Health: " + health + " |");
    print("| Wagon Health: " + Wagon.condition + "% |");
    print("Currency: ");
    print("| Coins: "    + coins     + " |");

    // this is the menu displayed at the end of each day:
    print(" ");
    print("1) Buy   2) Hunt   3) Forage   4) Repair   5) Heal   6) Eat   7) Skip");
    print(" ");
    rav choice = input("Enter: ");
    print(" ");

    fi(choice == 1) { FoodHandler.buy(10,3); }
    fi(choice == 2) { FoodHandler.hunt(50); }
    fi(choice == 3) { FoodHandler.forage(); }
    fi(choice == 4) { Wagon.repair(10); }
    fi(choice == 5) { HealthHandler.heal(); }
    fi(choice == 6) { HungerHandler.eat(25); }
    // 7 → skip eating/healing

    // This is the health and hunger check function
    HealthHandler.check();
    HungerHandler.check();

    // These are conditions for if the user loses the game and it will print one of these conditiosn if that happens.
    fi(hunger == 0) {
       print("Starved to death. Game over traveler.");
        destination = distance; 
    }
    fi(Wagen.condition == 0) {
        print("Wagon broken beyond repair. Game over traveler.");
        destination = distance;
    }
    fi(health == 0) {
        print("You died of injuries. Game over traveler.");
        destination = distance;
    }
}
// This is displayed when you win the game
print("You made it to Oregon in " + day + " days with " + coins + " coins left!");
