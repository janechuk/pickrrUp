-- Exported from QuickDBD: https://www.quickdatabasediagrams.com/
-- NOTE! If you have used non-SQL datatypes in your design, you will have to change these here.

-- Modify this code to update the DB schema diagram.
-- To reset the sample schema, replace everything with
-- two dots ('..' - without quotes).

CREATE TABLE "User" (
    "Username" string   NOT NULL,
    "Email" string   NOT NULL,
    "Password" string   NOT NULL,
    CONSTRAINT "pk_User" PRIMARY KEY (
        "Username"
     )
);

CREATE INDEX "idx_User_Email"
ON "User" ("Email");

