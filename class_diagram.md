# クラス図

```mermaid
classDiagram
    class Game
    class GameObject {
        <<Abstract>>
    }
    class City
    class Meteor
    class Missile
    class Explosion
    class MeteorManager
    class MissileManager
    class ExplosionsDetector

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
    Game --> ExplosionsDetector : references targets(City)
    Game --> ExplosionsDetector : references targets(UFO)


    ExplosionsDetector --> Explosion
    ExplosionsDetector --> GameObject : references targets (City, Meteor, Missile, UFO)

