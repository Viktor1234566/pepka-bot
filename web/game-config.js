// Game Configuration

const GAME_CONFIG = {
    // Player Stats
    PLAYER: {
        BASE_HP: 100,
        BASE_POWER: 125,
        LEVEL: 5,
        ATTACK_RANGE: 15
    },

    // Enemy Stats
    ENEMIES: {
        DRAGON: {
            HP: 100,
            POWER: 250,
            LEVEL: 8,
            ATTACK_DAMAGE: 15,
            ATTACK_SPEED: 2
        },
        GOBLIN: {
            HP: 30,
            POWER: 80,
            LEVEL: 2,
            ATTACK_DAMAGE: 5,
            ATTACK_SPEED: 1.5
        },
        ORC: {
            HP: 50,
            POWER: 150,
            LEVEL: 4,
            ATTACK_DAMAGE: 10,
            ATTACK_SPEED: 1.8
        }
    },

    // Battle Settings
    BATTLE: {
        ROUND_TIME: 5,
        MAX_ROUNDS: 5,
        COMBO_MULTIPLIER_PER_TAP: 0.1,
        MAX_COMBO_MULTIPLIER: 3,
        BASE_DAMAGE: 15,
        DAMAGE_VARIANCE: 10
    },

    // Rewards
    REWARDS: {
        VICTORY: {
            COINS: 500,
            XP: 250,
            STREAK: 1
        },
        DEFEAT: {
            XP: 10,
            STREAK_BREAK: true
        }
    },

    // Graphics
    GRAPHICS: {
        PARTICLE_COUNT: 10,
        PARTICLE_SIZE: 0.1,
        PARTICLE_LIFE: 30,
        CAMERA_DISTANCE: 15,
        ANIMATION_SPEED: 20
    },

    // Audio
    AUDIO: {
        ENABLED: true,
        MASTER_VOLUME: 0.8,
        SFX_VOLUME: 0.7,
        MUSIC_VOLUME: 0.5
    }
};

export default GAME_CONFIG;
