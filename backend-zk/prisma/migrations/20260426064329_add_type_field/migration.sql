-- RedefineTables
PRAGMA defer_foreign_keys=ON;
PRAGMA foreign_keys=OFF;
CREATE TABLE "new_cool_refuges" (
    "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "photo" TEXT,
    "longitude" REAL NOT NULL,
    "latitude" REAL NOT NULL,
    "name" TEXT NOT NULL,
    "type" TEXT NOT NULL DEFAULT 'library',
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
INSERT INTO "new_cool_refuges" ("city", "created_at", "facilities", "id", "latitude", "longitude", "name", "notes", "openingHours", "phone", "photo", "street", "updated_at", "website") SELECT "city", "created_at", "facilities", "id", "latitude", "longitude", "name", "notes", "openingHours", "phone", "photo", "street", "updated_at", "website" FROM "cool_refuges";
DROP TABLE "cool_refuges";
ALTER TABLE "new_cool_refuges" RENAME TO "cool_refuges";
PRAGMA foreign_keys=ON;
PRAGMA defer_foreign_keys=OFF;
