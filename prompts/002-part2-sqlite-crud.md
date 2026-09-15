# 002 - Part 2 SQLite CRUD scope

## Course requirements applied

- Use all four supplied CSV files to seed SQLite once.
- Keep application reads and writes in SQLite after seeding.
- Provide frontend search, simulated booking, booking history, cancellation that retains a history row, and test-booking deletion.
- Verify CRUD actions through browser and confirm persistence after browser refresh and backend restart.
- Develop substantial work on feature branch, merge reviewed work to main, preserve Part 1 checkpoint, and upload updated report.md.

## Project decisions

- Vue owns interactions and calls FastAPI only.
- FastAPI owns validation, booking ID generation, persistence, and database operations.
- One-time seed marker prevents deleted starter bookings from returning and prevents duplicate rows.
- Demo travelers are synthetic labels, not login accounts. No payments or live travel data are included.
