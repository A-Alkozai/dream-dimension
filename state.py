class State:

    # Global states
    GRAVITY = True
    RIGHT = False
    LEFT = False
    FLINCH = False
    DEAD = False

    # Player states
    IDLE = False

    SLOT1 = True
    SLOT2 = False
    SLOT3 = False
    SLOT4 = False

    GROUNDED = False
    JUMP = False
    IN_JUMP = False
    FALL = False

    INTERACT = False
    ON_LADDER = False
    CLIMB = False

    PUNCH = False
    PUNCH_END = False
    SHOOT = False

    # Enemy states
    ATTACK1 = False
    ATTACK1_COOLDOWN = False
    ATTACK2 = False
    ATTACK2_COOLDOWN = False
    ATTACK3 = False
    ATTACK3_COOLDOWN = False
    PATROL = False
