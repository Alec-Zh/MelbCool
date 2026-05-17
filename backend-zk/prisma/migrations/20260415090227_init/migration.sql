-- CreateTable
CREATE TABLE "cool_refuges" (
    "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "photo" TEXT,
    "longitude" REAL NOT NULL,
    "latitude" REAL NOT NULL,
    "name" TEXT NOT NULL,
    "openingHours" TEXT,
    "phone" TEXT,
    "city" TEXT NOT NULL,
    "street" TEXT NOT NULL,
    "website" TEXT,
    "facilities" TEXT,
    "notes" TEXT,
    "created_at" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" DATETIME NOT NULL
);
