# Telegram Sync System

A system designed to keep a Telegram repository (channel or group) fully synchronized with a **Source of Truth** repository. The project ensures that Telegram content always matches the authoritative data defined in the Source of Truth. Any message stored in the Source of Truth is automatically mirrored, updated, or restored in Telegram.

---

## Overview

This project implements a dual-repository architecture:

1. **Source of Truth Repository**
   The canonical storage for all valid messages. This is where official content is created, updated, or removed. The Telegram repository must always reflect this data.

2. **Telegram Repository**
   A Telegram channel or group that receives messages based on the Source of Truth. Messages are synchronized through the Telegram Bot API.

A synchronization engine continuously compares both repositories and enforces consistency. It sends missing messages, updates changed ones, and can optionally delete extra Telegram messages that are not present in the Source of Truth.

---

## Features

* Centralized Source of Truth for message management
* Automatic synchronization to Telegram
* Support for message creation, updates, and optional deletion
* Tracking of Telegram message IDs for precise updates
* Extensible design for additional storage backends or messaging platforms
* Suitable for automation, content pipelines, or controlled broadcasting

---

## How It Works

1. The system loads all messages from the Source of Truth repository.
2. It retrieves the current state of the Telegram repository using the Telegram Bot API.
3. It identifies differences between the two repositories.
4. It performs required actions:

   * Send missing messages
   * Edit outdated messages
   * Delete unwanted messages (optional)
5. It updates local mappings between Source-of-Truth items and Telegram message IDs.

---

## Requirements

* Python 3.9+
* Telegram Bot API token
* A backend for the Source of Truth (database or file-based system)
* Optional: Django, Celery, PostgreSQL (for advanced implementations)

---

## Setup

1. Clone the repository.
2. Install dependencies.
3. Configure the environment variables (Bot token, chat ID, database settings).
4. Run the synchronization script or enable periodic sync using a scheduler or worker.

---

## Use Cases

* Automated broadcasting systems
* Content approval workflows
* Maintaining consistent public channels
* Multi-platform publishing pipelines