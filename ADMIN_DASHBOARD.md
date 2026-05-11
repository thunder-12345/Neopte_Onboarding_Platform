# Admin Dashboard — Feature Guide

This guide walks through every section of the Admin Dashboard. It is written for anyone seeing the dashboard for the first time — no technical background required.

---

## Getting There

The Admin Dashboard is the home screen for any account with the **Admin** role. After logging in, admins are taken here automatically. You can also get back to it at any time by clicking **Home** in the top navigation bar.

---

## Page Header

At the top of the page you'll see the **Neopte Foundation logo**, the title "Admin Dashboard," and today's date displayed on the right. This is purely for orientation — it confirms you're on the admin view and shows when the data was last loaded (the page pulls fresh data every time it's opened).

---

## Section 1 — Org-Wide Stats

Four cards sit side by side near the top of the page, giving you an instant headcount of everyone on the platform:

| Card | What it shows |
|---|---|
| **Interns** | Number of accounts with the Intern role |
| **Volunteers** | Number of accounts with the Volunteer role |
| **Board Members** | Number of accounts with the Board role |
| **Pending Approvals** | Total number of items across the whole platform that are waiting for admin or board action |

The **Pending Approvals** card turns red and gets a highlighted border whenever the count is above zero. This makes it immediately obvious when something needs attention, even at a glance.

---

## Section 2 — Action Items

This is the dashboard's inbox. It lists every category of item that is sitting unresolved and waiting for someone to act on it. Each row shows a count badge on the left and a label describing what it is. Clicking any row takes you directly to the relevant management page.

**How the badges work:**
- **Red badge** — there are items that need attention
- **Green badge** — everything in this category is clear (count is zero)
- Rows with a zero count are shown in a muted/greyed style so the important ones stand out

**The four categories:**

### Hours submissions awaiting approval
Volunteers and interns log their hours through the platform. Each submission sits in "Pending" status until a board member or admin approves or denies it. The number here is how many are currently waiting. Clicking takes you to the Pending Hours page where you can review and take action on each one.

### Documents awaiting review
Members upload documents (forms, agreements, etc.) which go into a pending queue. The number shown is how many have been uploaded but not yet reviewed. Clicking takes you to the Pending Documents page.

### Task submissions awaiting grading
When an intern or volunteer marks a project task as complete, it enters a "done" status and waits for a board member to grade it. The count shown is how many submitted tasks have not been graded yet. Clicking takes you to the Task Status page, which shows pending reviews at the top.

### Accounts with no role assigned
When someone registers on the platform, they start with no role. They can log in but cannot access most features until an admin assigns them a role (Intern, Volunteer, Board, or Admin). This count shows how many accounts are in that unassigned state. Clicking takes you directly to the User List **already filtered** to show only those unassigned accounts — you don't have to set the filter yourself.

---

## Section 3 — Quick Actions

Three buttons for the most common admin tasks, so you don't have to dig through the navigation menu:

- **Create Task** — Opens the task creation form where you can assign a new project or reminder to a role group or specific users
- **View All Users** — Opens the full user list with search and filter tools
- **Activity Log** — Opens the full platform audit trail showing every action taken by every user

---

## Section 4 — Intern Progress

A table showing every intern on the platform and how they're doing at a glance. Each row is one intern.

**Columns:**

- **Intern** — The intern's name, which is a clickable link that takes you to their full task list
- **Tasks Done / Total** — A small progress bar plus a fraction (e.g. "3 / 5") showing how many of their assigned tasks they've completed vs. how many they have in total
- **Avg Grade** — The average score across all of their graded project tasks, expressed as a percentage. Shows a dash (—) if they haven't had any tasks graded yet
- **Pending** — How many tasks are still sitting in the "not started" state. A red badge means there are tasks they haven't touched yet; a green badge means everything is either submitted or graded

**Footer bar:** Below the table, a highlighted bar shows the **Overall Intern Task Completion Rate** — the percentage of all assigned intern tasks that have been completed across the entire cohort. This gives you a single number to gauge how the intern program is tracking overall.

If no intern accounts exist yet, the section shows a message instead of an empty table.

---

## Section 5 — Hours Overview

A panel showing the state of volunteer hours across the whole organization, scoped to the **current calendar month**.

**What's shown:**

- **Large number at the top** — Total approved volunteer hours for all time. This is the cumulative sum of every hours log that has been approved by a board member or admin
- **Pending approval note** — How many hours are currently submitted but not yet approved (in hours, not number of submissions)
- **Top Contributors This Month** — A short table of the top five people who have had the most hours approved in the current month, ranked highest to lowest. If no hours have been approved this month yet, a short message is shown instead

---

## Section 6 — Recent Activity

A live feed of the last 10 actions taken anywhere on the platform by any user. Each entry shows:

- **What happened** — The type of action (e.g. "Task completed," "Hours approved," "User role changed")
- **Who did it** — The name of the person who performed the action
- **When** — A relative timestamp: "just now," "5m ago," "2h ago," or "3d ago" depending on how long ago it occurred

This feed updates every time the page is loaded. It's useful for quickly spotting recent activity without having to open the full Activity Log — think of it as the highlights reel.

---

## A Note on Data Freshness

All numbers and tables on the Admin Dashboard are calculated live each time the page loads. There is no caching or scheduled refresh. To see the most current state of the platform, simply reload the page.
