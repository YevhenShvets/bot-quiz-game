CREATE TABLE "Game"(
    "id" SERIAL NOT NULL,
    "chat_id" INTEGER NOT NULL,
    "number" INTEGER NOT NULL,
    "isActive" BOOLEAN NOT NULL,
    "last_user_id" INTEGER NOT NULL
);
ALTER TABLE
    "Game" ADD PRIMARY KEY("id");
CREATE TABLE "GameUsers"(
    "game_id" INTEGER NOT NULL,
    "user_id" INTEGER NOT NULL,
    "user_stat" INTEGER NOT NULL
);
CREATE TABLE "GameWords"(
    "id" SERIAL NOT NULL,
    "game_id" INTEGER NOT NULL,
    "word" VARCHAR(255) NOT NULL,
    "user_id" INTEGER NOT NULL
);
ALTER TABLE
    "GameWords" ADD PRIMARY KEY("id");
CREATE TABLE "UsersStats"(
    "user_id" INTEGER NOT NULL,
    "stat" INTEGER NOT NULL
);
ALTER TABLE
    "UsersStats" ADD PRIMARY KEY("user_id");
CREATE TABLE "Users"(
    "telegram_id" INTEGER NOT NULL,
    "full_name" VARCHAR(255) NOT NULL
);
ALTER TABLE
    "Users" ADD PRIMARY KEY("telegram_id");
ALTER TABLE
    "GameWords" ADD CONSTRAINT "gamewords_game_id_foreign" FOREIGN KEY("game_id") REFERENCES "Game"("id");
ALTER TABLE
    "GameUsers" ADD CONSTRAINT "gameusers_game_id_foreign" FOREIGN KEY("game_id") REFERENCES "Game"("id");
ALTER TABLE
    "GameUsers" ADD CONSTRAINT "gameusers_user_id_foreign" FOREIGN KEY("user_id") REFERENCES "Users"("telegram_id");