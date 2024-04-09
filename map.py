from vector import Vector
from entity import Entity
from portal import Portal
from enemy import Enemy
import json
import random


class MapManager:
    def __init__(self, game_manager=None, **kwargs):
        super().__init__(**kwargs)
        self.game_manager = game_manager
        self.tile_size = 60
        self.tiles = set()

        self.current_room_index = 0

        with open("map.json", "r") as f:
            self.map_data = json.load(f)

    def change_room(self, direction):
        self.current_room_index += direction
        self.game_manager.score_counter.update_level(self.current_room_index)
        self.game_manager.clear_screen()
        self.game_manager.add_entity(self.game_manager.player)

        # save player health
        self.game_manager.player_health = self.game_manager.player.lives
        self.load()

        self.game_manager.player.lives = self.game_manager.player_health

    def load(self):
        self.x, self.y = 0, 0

        for i, row in enumerate(self.map_data[self.current_room_index]):
            for j, cell in enumerate(row):
                if cell == ' ':
                    continue

                cell_pos = Vector(
                    self.tile_size * j + self.tile_size / 2,
                    self.tile_size * i + self.tile_size / 2
                )
                cell_image = self.get_tile_image(cell)

                match cell:
                    # Dungeon <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
                    case 'df1':
                        entity_kind = 'block'
                        entity_name = 'd_floor'
                        block_entity = Entity(kind=entity_kind, name=entity_name, position=cell_pos, img_url=cell_image,
                                              img_dest_dim=(60, 60))
                    case 'df2':
                        entity_kind = 'block'
                        entity_name = 'd_floor'
                        block_entity = Entity(kind=entity_kind, name=entity_name, position=cell_pos, img_url=cell_image,
                                              img_dest_dim=(60, 60))
                    case 'df3':
                        entity_kind = 'block'
                        entity_name = 'd_floor'
                        block_entity = Entity(kind=entity_kind, name=entity_name, position=cell_pos, img_url=cell_image,
                                              img_dest_dim=(60, 60))
                    case 'dc1':
                        entity_kind = 'block'
                        entity_name = 'd_ceiling'
                        block_entity = Entity(kind=entity_kind, name=entity_name, position=cell_pos, img_url=cell_image,
                                              img_dest_dim=(60, 60))
                    case 'dc2':
                        entity_kind = 'block'
                        entity_name = 'd_ceiling'
                        block_entity = Entity(kind=entity_kind, name=entity_name, position=cell_pos, img_url=cell_image,
                                              img_dest_dim=(60, 60))
                    case 'dc3':
                        entity_kind = 'block'
                        entity_name = 'd_ceiling'
                        block_entity = Entity(kind=entity_kind, name=entity_name, position=cell_pos, img_url=cell_image,
                                              img_dest_dim=(60, 60))
                    case 'dc':
                        entity_kind = 'cavity'
                        entity_name = 'd_cavity'
                        block_entity = Entity(kind=entity_kind, name=entity_name, position=cell_pos, img_url=cell_image,
                                              img_dest_dim=(60, 60))
                    case 'drw':
                        entity_kind = 'block'
                        entity_name = 'd_wall'
                        block_entity = Entity(kind=entity_kind, name=entity_name, position=cell_pos, img_url=cell_image,
                                              img_dest_dim=(60, 60))
                    case 'dlw':
                        entity_kind = 'block'
                        entity_name = 'd_wall'
                        block_entity = Entity(kind=entity_kind, name=entity_name, position=cell_pos, img_url=cell_image,
                                              img_dest_dim=(60, 60))
                    case 'db1':
                        entity_kind = 'block'
                        entity_name = 'd_wall'
                        block_entity = Entity(kind=entity_kind, name=entity_name, position=cell_pos, img_url=cell_image,
                                              img_dest_dim=(60, 60))
                    case 'db2':
                        entity_kind = 'block'
                        entity_name = 'd_wall'
                        block_entity = Entity(kind=entity_kind, name=entity_name, position=cell_pos, img_url=cell_image,
                                              img_dest_dim=(60, 60))
                    case 'dl':
                        entity_kind = 'ladder'
                        entity_name = 'd_ladder'
                        block_entity = Entity(kind=entity_kind, name=entity_name, position=cell_pos, img_url=cell_image,
                                              img_dest_dim=(60, 60))
                    case 'dp1':
                        entity_kind = 'block'
                        entity_name = 'd_wall'
                        block_entity = Entity(kind=entity_kind, name=entity_name, position=cell_pos, img_url=cell_image,
                                              img_dest_dim=(60, 60))
                    case 'dp2':
                        entity_kind = 'block'
                        entity_name = 'd_wall'
                        block_entity = Entity(kind=entity_kind, name=entity_name, position=cell_pos, img_url=cell_image,
                                              img_dest_dim=(60, 60))
                    case 'dp3':
                        entity_kind = 'block'
                        entity_name = 'd_wall'
                        block_entity = Entity(kind=entity_kind, name=entity_name, position=cell_pos, img_url=cell_image,
                                              img_dest_dim=(60, 60))
                    case 'dw1':
                        entity_kind = 'block'
                        entity_name = 'd_wall'
                        block_entity = Entity(kind=entity_kind, name=entity_name, position=cell_pos, img_url=cell_image,
                                              img_dest_dim=(60, 120))
                    case 'dw2':
                        entity_kind = 'block'
                        entity_name = 'd_wall'
                        block_entity = Entity(kind=entity_kind, name=entity_name, position=cell_pos, img_url=cell_image,
                                              img_dest_dim=(60, 120))
                    case 'dw3':
                        entity_kind = 'block'
                        entity_name = 'd_wall'
                        block_entity = Entity(kind=entity_kind, name=entity_name, position=cell_pos, img_url=cell_image,
                                              img_dest_dim=(60, 120))
                    case 'sr':
                        entity_kind = 'cavity'
                        entity_name = 'sign'
                        block_entity = Entity(kind=entity_kind, name=entity_name, position=cell_pos, img_url=cell_image,
                                              img_dest_dim=(60, 60))
                    case 'sl':
                        entity_kind = 'cavity'
                        entity_name = 'sign'
                        block_entity = Entity(kind=entity_kind, name=entity_name, position=cell_pos, img_url=cell_image,
                                              img_dest_dim=(60, 60))

                    # Jungle <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
                    case 'jf':
                        entity_kind = 'block'
                        entity_name = 'f_floor'
                        block_entity = Entity(kind=entity_kind, name=entity_name, position=cell_pos, img_url=cell_image,
                                              img_dest_dim=(60, 60))
                    case 'jfrw':
                        entity_kind = 'block'
                        entity_name = 'f_floor'
                        block_entity = Entity(kind=entity_kind, name=entity_name, position=cell_pos, img_url=cell_image,
                                              img_dest_dim=(60, 60))
                    case 'jflw':
                        entity_kind = 'block'
                        entity_name = 'f_floor'
                        block_entity = Entity(kind=entity_kind, name=entity_name, position=cell_pos, img_url=cell_image,
                                              img_dest_dim=(60, 60))
                    case 'jfc':
                        entity_kind = 'block'
                        entity_name = 'f_floor'
                        block_entity = Entity(kind=entity_kind, name=entity_name, position=cell_pos, img_url=cell_image,
                                              img_dest_dim=(60, 60))
                    case 'jfl':
                        entity_kind = 'block'
                        entity_name = 'f_floor'
                        block_entity = Entity(kind=entity_kind, name=entity_name, position=cell_pos, img_url=cell_image,
                                              img_dest_dim=(60, 60))
                    case 'jfr':
                        entity_kind = 'block'
                        entity_name = 'f_floor'
                        block_entity = Entity(kind=entity_kind, name=entity_name, position=cell_pos, img_url=cell_image,
                                              img_dest_dim=(60, 60))
                    case 'jc':
                        entity_kind = 'cavity'
                        entity_name = 'j_cavity'
                        block_entity = Entity(kind=entity_kind, name=entity_name, position=cell_pos, img_url=cell_image,
                                              img_dest_dim=(60, 60))
                    case 'jw1':
                        entity_kind = 'block'
                        entity_name = 'j_wall'
                        block_entity = Entity(kind=entity_kind, name=entity_name, position=cell_pos, img_url=cell_image,
                                              img_dest_dim=(120, 60))
                    case 'jw2':
                        entity_kind = 'block'
                        entity_name = 'j_wall'
                        block_entity = Entity(kind=entity_kind, name=entity_name, position=cell_pos, img_url=cell_image,
                                              img_dest_dim=(120, 60))
                    case 'jp1':
                        entity_kind = 'block'
                        entity_name = 'j_floor'
                        block_entity = Entity(kind=entity_kind, name=entity_name, position=cell_pos, img_url=cell_image,
                                              img_dest_dim=(60, 90))
                    case 'jp2':
                        entity_kind = 'block'
                        entity_name = 'j_floor'
                        block_entity = Entity(kind=entity_kind, name=entity_name, position=cell_pos, img_url=cell_image,
                                              img_dest_dim=(60, 90))
                    case 'jp1.1':
                        entity_kind = 'block'
                        entity_name = 'bush_floor'
                        block_entity = Entity(kind=entity_kind, name=entity_name, position=cell_pos, img_url=cell_image,
                                              img_dest_dim=(60, 90))
                    case 'jp1.2':
                        entity_kind = 'block'
                        entity_name = 'bush_floor'
                        block_entity = Entity(kind=entity_kind, name=entity_name, position=cell_pos, img_url=cell_image,
                                              img_dest_dim=(60, 90))
                    case 'jp1.3':
                        entity_kind = 'block'
                        entity_name = 'bush_floor'
                        block_entity = Entity(kind=entity_kind, name=entity_name, position=cell_pos, img_url=cell_image,
                                              img_dest_dim=(60, 90))
                    case 'jrp1':
                        entity_kind = 'block'
                        entity_name = 'j_floor'
                        block_entity = Entity(kind=entity_kind, name=entity_name, position=cell_pos, img_url=cell_image,
                                              img_dest_dim=(60, 60))
                    case 'jrp2':
                        entity_kind = 'block'
                        entity_name = 'j_floor'
                        block_entity = Entity(kind=entity_kind, name=entity_name, position=cell_pos, img_url=cell_image,
                                              img_dest_dim=(60, 60))
                    case 'jrp3':
                        entity_kind = 'block'
                        entity_name = 'j_floor'
                        block_entity = Entity(kind=entity_kind, name=entity_name, position=cell_pos, img_url=cell_image,
                                              img_dest_dim=(60, 60))
                    case 'jgp1':
                        entity_kind = 'block'
                        entity_name = 'j_floor'
                        block_entity = Entity(kind=entity_kind, name=entity_name, position=cell_pos, img_url=cell_image,
                                              img_dest_dim=(60, 60))
                    case 'jgp2':
                        entity_kind = 'block'
                        entity_name = 'j_floor'
                        block_entity = Entity(kind=entity_kind, name=entity_name, position=cell_pos, img_url=cell_image,
                                              img_dest_dim=(60, 60))
                    case 'jgp3':
                        entity_kind = 'block'
                        entity_name = 'j_floor'
                        block_entity = Entity(kind=entity_kind, name=entity_name, position=cell_pos, img_url=cell_image,
                                              img_dest_dim=(60, 60))
                    case 'jrf1':
                        entity_kind = 'block'
                        entity_name = 'j_floor'
                        block_entity = Entity(kind=entity_kind, name=entity_name, position=cell_pos, img_url=cell_image,
                                              img_dest_dim=(60, 60))
                    case 'jrf2':
                        entity_kind = 'block'
                        entity_name = 'j_floor'
                        block_entity = Entity(kind=entity_kind, name=entity_name, position=cell_pos, img_url=cell_image,
                                              img_dest_dim=(60, 60))
                    # Universal <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
                    case 'l':
                        entity_kind = 'ladder'
                        block_entity = Entity(kind=entity_kind, position=cell_pos, img_url=cell_image,
                                              img_dest_dim=(60, 60))
                    case 'h':
                        entity_kind = 'drop'
                        entity_name = 'heart'
                        block_entity = Entity(kind=entity_kind, name=entity_name, position=cell_pos, img_url=cell_image,
                                              img_dest_dim=(40, 40))
                    case 't1':
                        entity_kind = 'drop'
                        entity_name = 't1'
                        block_entity = Entity(kind=entity_kind, name=entity_name, position=cell_pos, img_url=cell_image,
                                              img_dest_dim=(40, 40))
                    case 't2':
                        entity_kind = 'drop'
                        entity_name = 't2'
                        block_entity = Entity(kind=entity_kind, name=entity_name, position=cell_pos, img_url=cell_image,
                                              img_dest_dim=(40, 40))
                    case 't3':
                        entity_kind = 'drop'
                        entity_name = 't3'
                        block_entity = Entity(kind=entity_kind, name=entity_name, position=cell_pos, img_url=cell_image,
                                              img_dest_dim=(40, 40))
                    case 't4':
                        entity_kind = 'drop'
                        entity_name = 't4'
                        block_entity = Entity(kind=entity_kind, name=entity_name, position=cell_pos, img_url=cell_image,
                                              img_dest_dim=(40, 40))
                    case 't5':
                        entity_kind = 'drop'
                        entity_name = 't5'
                        block_entity = Entity(kind=entity_kind, name=entity_name, position=cell_pos, img_url=cell_image,
                                              img_dest_dim=(40, 40))
                    case 't6':
                        entity_kind = 'drop'
                        entity_name = 't6'
                        block_entity = Entity(kind=entity_kind, name=entity_name, position=cell_pos, img_url=cell_image,
                                              img_dest_dim=(40, 40))
                    case 't7':
                        entity_kind = 'drop'
                        entity_name = 't7'
                        block_entity = Entity(kind=entity_kind, name=entity_name, position=cell_pos, img_url=cell_image,
                                              img_dest_dim=(40, 40))
                    case 't8':
                        entity_kind = 'drop'
                        entity_name = 't8'
                        block_entity = Entity(kind=entity_kind, name=entity_name, position=cell_pos, img_url=cell_image,
                                              img_dest_dim=(40, 40))
                    case 't9':
                        entity_kind = 'drop'
                        entity_name = 't9'
                        block_entity = Entity(kind=entity_kind, name=entity_name, position=cell_pos, img_url=cell_image,
                                              img_dest_dim=(40, 40))
                    case 't10':
                        entity_kind = 'drop'
                        entity_name = 't10'
                        block_entity = Entity(kind=entity_kind, name=entity_name, position=cell_pos, img_url=cell_image,
                                              img_dest_dim=(40, 40))
                    case 't11':
                        entity_kind = 'drop'
                        entity_name = 't11'
                        block_entity = Entity(kind=entity_kind, name=entity_name, position=cell_pos, img_url=cell_image,
                                              img_dest_dim=(40, 40))
                    case 't12':
                        entity_kind = 'drop'
                        entity_name = 't12'
                        block_entity = Entity(kind=entity_kind, name=entity_name, position=cell_pos, img_url=cell_image,
                                              img_dest_dim=(40, 40))
                    case 'lr':
                        entity_kind = 'drop'
                        entity_name = 'learn_red'
                        block_entity = Entity(kind=entity_kind, name=entity_name, position=cell_pos, img_url=cell_image,
                                              img_dest_dim=(50, 50))
                    case 'lp':
                        entity_kind = 'drop'
                        entity_name = 'learn_purple'
                        block_entity = Entity(kind=entity_kind, name=entity_name, position=cell_pos, img_url=cell_image,
                                              img_dest_dim=(50, 50))
                    case 'lsp1':
                        entity_kind = 'drop'
                        entity_name = 'learn_sp1'
                        block_entity = Entity(kind=entity_kind, name=entity_name, position=cell_pos, img_url=cell_image,
                                              img_dest_dim=(50, 50))
                    case 'lsp2':
                        entity_kind = 'drop'
                        entity_name = 'learn_sp2'
                        block_entity = Entity(kind=entity_kind, name=entity_name, position=cell_pos, img_url=cell_image,
                                              img_dest_dim=(50, 50))
                    case 'p':
                        entity_kind = 'portal'
                        block_entity = Portal(kind=entity_kind, position=cell_pos, img_url=cell_image,
                                              img_dest_dim=(60, 60), game_manager=self.game_manager, animated=True,
                                              column=5)
                    case 's':
                        self.game_manager.player.position = cell_pos
                    # Forest Enemies <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
                    case 'fe':
                        entity_kind = 'enemy'
                        enemies = [
                            Enemy(kind=entity_kind, name='warrior', is_ranged=False,
                                  walk_frames=3, jump_frames=2, attack_frames=3, flinch_frames=2,
                                  velocity=Vector(0, 0), speed=0.6, img_url="images/sprites/enemies/orc_warrior.png",
                                  img_dest_dim=(60, 60), position=cell_pos, row=7, column=4,
                                  game_manager=self.game_manager, health=1),
                            Enemy(kind=entity_kind, name='hunter', is_ranged=True,
                                  walk_frames=3, jump_frames=2, attack_frames=4, flinch_frames=2,
                                  velocity=Vector(0, 0), speed=0.3, img_url="images/sprites/enemies/orc_hunter.png",
                                  img_dest_dim=(60, 60), cooldown=40, position=cell_pos, row=7, column=8,
                                  game_manager=self.game_manager, health=random.randint(1, 2)),
                            Enemy(kind=entity_kind, name='shaman', is_ranged=True,
                                  walk_frames=3, jump_frames=2, attack_frames=4, flinch_frames=2,
                                  velocity=Vector(0, 0), speed=0.3, img_url="images/sprites/enemies/orc_shaman.png",
                                  img_dest_dim=(60, 60), cooldown=40, position=cell_pos, row=7, column=8,
                                  game_manager=self.game_manager, health=random.randint(1, 2))
                        ]
                        block_entity = random.choice(enemies)
                    # Dungeon Enemies <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
                    case 'de':
                        entity_kind = 'enemy'
                        enemies = [
                            Enemy(kind=entity_kind, name='fighter', is_ranged=False,
                                  walk_frames=4, attack_frames=4, flinch_frames=2,
                                  velocity=Vector(0, 0), img_url='images/sprites/enemies/skeleton_fighter.png',
                                  img_dest_dim=(40, 60), cooldown=40, position=cell_pos, row=7, column=4, speed=0.9,
                                  game_manager=self.game_manager, health=random.randint(1, 2), points=2),
                            Enemy(kind=entity_kind, name='swordsman', is_ranged=False,
                                  walk_frames=4, attack_frames=4, flinch_frames=2,
                                  velocity=Vector(0, 0), img_url='images/sprites/enemies/skeleton_swordsman.png',
                                  img_dest_dim=(50, 70), cooldown=40, position=cell_pos, row=7, column=4, speed=0.8,
                                  game_manager=self.game_manager, health=random.randint(1, 2)+0.5, points=3),
                            Enemy(kind=entity_kind, name='bomber', is_ranged=False,
                                  walk_frames=4, attack_frames=1, flinch_frames=2,
                                  velocity=Vector(0, 0), img_url='images/sprites/enemies/skeleton_bomber.png',
                                  img_dest_dim=(50, 70), cooldown=1, position=cell_pos, row=7, column=4, speed=0.7,
                                  game_manager=self.game_manager, health=random.randint(1, 2), points=2)
                        ]
                        block_entity = random.choice(enemies)

                self.game_manager.add_entity(block_entity)

    def get_tile_image(self, char) -> str:
        match char:
            case 'df1': return 'images/dungeon/floor1.png'
            case 'df2': return 'images/dungeon/floor2.png'
            case 'df3': return 'images/dungeon/floor3.png'
            case 'drw': return 'images/dungeon/right_wall.png'
            case 'dc': return 'images/dungeon/cavity.png'
            case 'dlw': return 'images/dungeon/left_wall.png'
            case 'dc1': return 'images/dungeon/ceiling1.png'
            case 'dc2': return 'images/dungeon/ceiling2.png'
            case 'dc3': return 'images/dungeon/ceiling3.png'

            case 'db1': return 'images/dungeon/brick1.png'
            case 'db2': return 'images/dungeon/brick2.png'
            case 'dl': return 'images/dungeon/ladder.png'
            case 'dp1': return 'images/dungeon/platform1.png'
            case 'dp2': return 'images/dungeon/platform2.png'
            case 'dp3': return 'images/dungeon/platform3.png'
            case 'dw1': return 'images/dungeon/wood_platform1.png'
            case 'dw2': return 'images/dungeon/wood_platform2.png'
            case 'dw3': return 'images/dungeon/wood_platform3.png'
            case 'sr': return 'images/dungeon/sign_R.png'
            case 'sl': return 'images/dungeon/sign_L.png'

            case 'jf': return 'images/jungle/Floor.png'
            case 'jfl': return 'images/jungle/FloorL.png'
            case 'jfr': return 'images/jungle/FloorR.png'
            case 'jfc': return 'images/jungle/FloorT.png'
            case 'jflw': return 'images/jungle/FloorLW.png'
            case 'jfrw': return 'images/jungle/FloorRW.png'
            case 'jc': return 'images/jungle/Floor_Cavity.png'

            case 'jrp1': return 'images/jungle/RockyPlatform1.png'
            case 'jrp2': return 'images/jungle/RockyPlatform2.png'
            case 'jrp3': return 'images/jungle/RockyPlatform3.png'

            case 'jgp1': return 'images/jungle/GrassyPlatform1.png'
            case 'jgp2': return 'images/jungle/GrassyPlatform2.png'
            case 'jgp3': return 'images/jungle/GrassyPlatform3.png'
            case 'jrf1': return 'images/jungle/Rock1.png'
            case 'jrf2': return 'images/jungle/Rock2.png'

            case 'jw1': return 'images/jungle/Wall1.png'
            case 'jw2': return 'images/jungle/Wall2.png'

            case 'jp1': return 'images/jungle/Branch_Mid1.png'
            case 'jp2': return 'images/jungle/Branch_Mid2.png'
            case 'jp1.1': return 'images/jungle/Branch_LeftLeaf.png'
            case 'jp1.2': return 'images/jungle/Branch_MidLeaf.png'
            case 'jp1.3': return 'images/jungle/Branch_RightLeaf.png'

            case 'l': return 'images/ladder.png'
            case 'h': return 'images/heart.png'
            case 'lr': return 'images/interactables/learn_red.png'
            case 'lp': return 'images/interactables/learn_purple.png'
            case 'lsp1': return 'images/interactables/learn_sp1.png'
            case 'lsp2': return 'images/interactables/learn_sp2.png'
            case 'p': return 'images/portal.png'

            case 't1' | 't2' | 't3' | 't4' | 't5' | 't6' | 't7' | 't8'| 't9'| 't10'| 't11' | 't12': return 'images/interactables/info.png'

        return ' '
