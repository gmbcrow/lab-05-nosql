
#!/usr/bin/env python3
"""Print a report of the books linked to selected authors in the bookstore database."""

import logging
import os

import pymongo

# Credentials come from environment variables, never hardcoded
MONGODB_ATLAS_URL = os.environ.get("MONGODB_ATLAS_URL")
MONGODB_ATLAS_USER = os.environ.get("MONGODB_ATLAS_USER")
MONGODB_ATLAS_PWD = os.environ.get("MONGODB_ATLAS_PWD")

# Report status messages (connection success, errors) with timestamps
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")


def print_author_report(authors, books, author_ids):
    """Print each author's name with the title and year of every linked book.

    authors, books: PyMongo collections
    author_ids: list of author _id values to include in the report
    """
    # Count how many of the requested authors exist in the collection
    total = authors.count_documents({"_id": {"$in": author_ids}})
    print(f"Authors: {total}\n")

    for author_id in author_ids:
        # Look up the author document by its _id
        author = authors.find_one({"_id": author_id})
        if author is None:
            logging.warning("No author found with _id %s", author_id)
            continue

        print(author["name"])
        # The join: find every book whose author_ids array contains this author's _id
        for book in books.find({"author_ids": author["_id"]}):
            print(f"  {book['title']} ({book['published_year']})")
        print()


def main():
    """Connect to MongoDB Atlas, then print the report for the chosen authors."""
    # Stop early if the environment variables are not set in this shell
    if not (MONGODB_ATLAS_URL and MONGODB_ATLAS_USER and MONGODB_ATLAS_PWD):
        logging.error("Set MONGODB_ATLAS_URL, MONGODB_ATLAS_USER and MONGODB_ATLAS_PWD first")
        return

    client = None
    try:
        # Open the connection using the credentials from the environment
        client = pymongo.MongoClient(
            MONGODB_ATLAS_URL,
            username=MONGODB_ATLAS_USER,
            password=MONGODB_ATLAS_PWD,
        )
        # Ping the server so a bad connection fails here, with a clear message
        client.admin.command("ping")
        logging.info("Connected to MongoDB Atlas")

        # Select the database and the two collections
        db = client["bookstore"]
        authors = db["authors"]
        books = db["books"]

        # Two loaded authors (Gaiman, Pratchett) plus the one added in Case Study 1
        author_ids = ["author_002", "author_003", "author_004"]

        print_author_report(authors, books, author_ids)
    except Exception as err:
        logging.error("Something went wrong: %s", err)
    finally:
        # Always close the client, even if an error happened
        if client is not None:
            client.close()
            logging.info("Connection closed")


# Run main() only when this file is executed directly
if __name__ == "__main__":
    main()
