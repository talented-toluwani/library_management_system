# Vantag Library Management System

A command-line Python application for managing a library's books and users. Built with object-oriented programming principles including abstract classes, inheritance, encapsulation, custom exceptions, static methods, and JSON-based data persistence.

---

##  Overview

The Vantag Library Management System allows users to register accounts, borrow and return books, search the catalog, and add new titles — all through an interactive CLI. Data is persisted across sessions using JSON files, so the library's state is never lost between runs.

---

## Features

-  **Borrow & Return Books** — Tracks which books are available, borrowed, and by whom
- **Role-Based Access** — Students have a 3-book borrow limit; Admins have no limit
- **Book Search** — Case-insensitive partial matching across the catalog
- **Add New Books** — Extend the library catalog with duplicate detection
- **User Registration** — Register new students or admins with email-based uniqueness checks
- **JSON Persistence** — Books, users, and borrowed records are saved and reloaded across sessions
- **Custom Exception** — `BookUnavailableError` for clear, descriptive borrowing failures

---

## Project Structure

```
vantag_library/
│
├── main.py               # All classes and the run() entry point
├── books.json            # Persisted book catalog (auto-created)
├── users.json            # Persisted registered users (auto-created)
├── borrowed.json         # Persisted borrowed books log (auto-created)
└── README.md
```

---

## Architecture & Class Design

```
LibraryUser (ABC)
├── StudentUser          ← max 3 books, inherits LibraryUser
└── AdminUser            ← no limit, inherits LibraryUser

Book                     ← represents a single book, handles borrow/return state
BookUnavailableError     ← custom exception for unavailable books

LibraryPersistence       ← static methods: save_data(), load_data()
LibrarySearch            ← static method: search()

Library                  ← main orchestrator: add_books(), register_user(),
                            borrow_book(), return_book()
```

### Key OOP Concepts Applied

| Concept | Where Used |
|---------|-----------|
| **Abstract Class** | `LibraryUser` — enforces `view_access()` in all subclasses |
| **Inheritance** | `StudentUser` and `AdminUser` extend `LibraryUser` |
| **Encapsulation** | `_isbn` (Book) and `_borrowed_books` (LibraryUser) are protected attributes |
| **Custom Exception** | `BookUnavailableError` gives meaningful borrowing error messages |
| **Static Methods** | `LibraryPersistence` and `LibrarySearch` use `@staticmethod` — no instance needed |
| **Polymorphism** | `view_access()` behaves differently for student vs admin |

---

## ⚙️ How It Works

### Borrowing Logic

```
If StudentUser:
    Check if borrowed count >= 3 → reject if over limit
    Otherwise → call _process_borrow_book()

If AdminUser:
    No limit check → call _process_borrow_book() directly

_process_borrow_book():
    If book not in catalog → raise BookUnavailableError
    Remove from books list → add to borrowed_books → save both to JSON
```

### Persistence Flow

```
On startup:  load books.json, users.json, borrowed.json → populate in-memory lists
On change:   LibraryPersistence.save_data() → write updated list back to JSON
```

---

## Class Reference

| Class | Responsibility |
|-------|---------------|
| `Book` | Represents a book; handles `mark_borrowed()` and `mark_returned()` |
| `LibraryUser` | Abstract base class for all user types |
| `StudentUser` | Library user with a 3-book borrow cap |
| `AdminUser` | Library user with no borrow cap |
| `BookUnavailableError` | Custom exception raised when a requested book isn't in the catalog |
| `LibraryPersistence` | Handles all JSON read/write operations |
| `LibrarySearch` | Provides case-insensitive partial search across the book catalog |
| `Library` | Main orchestrator — manages books, users, borrowing, and returning |

---

## Getting Started

### Prerequisites

- Python 3.8 or higher
- No external dependencies — uses Python standard library only (`json`, `os`, `abc`)

### Installation

```bash
# Clone the repository
git clone https://github.com/your-username/vantag-library.git

# Navigate into the project directory
cd vantag-library
```

### Running the App

```bash
python main.py
```

The JSON files (`books.json`, `users.json`, `borrowed.json`) are created automatically on first run.

---

## Sample Output

```
=== Welcome to the Vantag Library Management System ===

Title: Fairy tale, Author: Mary Jen, ISBN: 1235, Available: Yes

Enter in valid name: Jane Doe
Enter in a valid email: jane@gmail.com
Are you a student or an admin?: student
New user has been successfully registered

Student can borrow a maximum of three books
What book do you want to borrow?: Mary In Wonder Land
Book has been successfully borrowed.

As a student you can borrow 3 books
```

---

## Error Handling

| Scenario | Handled By |
|----------|-----------|
| Book not in catalog | `BookUnavailableError` → descriptive message |
| Student borrow limit reached | Guard check in `borrow_book()` → prints limit message |
| JSON file not found on load | `os.path.exists()` check → starts with default data |
| Malformed JSON file | `json.JSONDecodeError` → returns empty list gracefully |
| Duplicate user registration | Email uniqueness check in `register_user()` |
| Duplicate book addition | Title check in `add_books()` before appending |
| Invalid role on registration | Validated against `["student", "admin"]` |
| Book not in user's borrow list on return | Checked before processing return |

---

## Key Learnings

Building this project deepened my understanding of:

- Designing class hierarchies using **abstract base classes** (`ABC`) to enforce contracts
- Applying **encapsulation** with protected attributes to manage data access
- Using **`@staticmethod`** for utility classes that don't need instance state
- Implementing a **custom exception class** for domain-specific error handling
- Persisting application state with `json.dump()` / `json.load()` across sessions
- Writing **defensive logic** for edge cases: duplicate users, borrow limits, missing books

---

##  Potential Improvements

- [ ] Add a proper interactive CLI menu instead of calling functions directly in `run()`
- [ ] Implement login/authentication so borrow records are tied to verified users
- [ ] Store `Book` objects as JSON (serializing attributes) instead of plain strings
- [ ] Add a due-date system with overdue tracking
- [ ] Write unit tests for borrow/return logic and search functionality
- [ ] Migrate storage to SQLite for more robust querying

---

## Author

**Miracle**  
Software Engineering Student — Bowen University, Iwo, Nigeria  
🔗 [GitHub Profile](https://github.com/your-username)

---
