# クラス図

```mermaid
classDiagram
    class Game
    class GameObject {
        <<Abstract>>
    }
    class MeteorManager
    class MissileManager
    class UFOManager
    class ExplosionsDetector
    class Explosion
    class Base
    class City
    class Meteor
    class Missile
    class UFO

    direction BT
    City --|> GameObject
    Meteor --|> GameObject
    Missile --|> GameObject
    Base --|> GameObject
    UFO --|> GameObject

    MeteorManager --> Meteor
    MeteorManager --> Explosion
    MissileManager --> Missile
    MissileManager --> Explosion
    MissileManager --> Base
    UFOManager --> UFO

    Game --> MeteorManager
    Game --> MissileManager
    Game --> UFOManager
    Game --> ExplosionsDetector : references targets(Meteor)
    Game --> ExplosionsDetector : references targets(City,Base)
    Game --> ExplosionsDetector : references targets(UFO)

    ExplosionsDetector --> Explosion
    ExplosionsDetector --> GameObject : references targets (City, Base, Meteor, Missile, UFO)
