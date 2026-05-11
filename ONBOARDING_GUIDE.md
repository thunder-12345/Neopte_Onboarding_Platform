# Neopte Platform — Step-by-Step Onboarding Guide

This guide is for anyone using the Neopte onboarding platform for the first time. It covers everything from creating your account to completing tasks, logging hours, uploading documents, and — if you are a board member — managing users, creating assignments, and grading submissions. No prior knowledge of the platform is assumed.

---

## Table of Contents

1. [Understanding User Roles](#1-understanding-user-roles)
2. [Getting Started — All Users](#2-getting-started--all-users)
   - [Registering an Account](#21-registering-an-account)
   - [Logging In](#22-logging-in)
   - [Editing Your Profile](#23-editing-your-profile)
   - [Navigating Your Dashboard](#24-navigating-your-dashboard)
3. [For Volunteers & Interns](#3-for-volunteers--interns)
   - [Logging Hours](#31-logging-hours)
   - [Uploading Documents](#32-uploading-documents)
   - [Managing Your Tasks](#33-managing-your-tasks)
   - [Completing a Task](#34-completing-a-task)
   - [Viewing Your Grades](#35-viewing-your-grades)
   - [Downloading Your Certificate](#36-downloading-your-certificate)
4. [For Board Members](#4-for-board-members)
   - [Approving Hours](#41-approving-hours)
   - [Approving Documents](#42-approving-documents)
   - [Creating an Assignment](#43-creating-an-assignment)
   - [Grading a Task Submission](#44-grading-a-task-submission)
   - [Sending a Task Back for Revision](#45-sending-a-task-back-for-revision)
   - [Managing Users](#46-managing-users)
   - [Activity Log & Notifications](#47-activity-log--notifications)
5. [Common End-to-End Workflows](#5-common-end-to-end-workflows)
   - [New Volunteer Getting Started](#51-new-volunteer-getting-started)
   - [Board Onboarding a New Cohort](#52-board-onboarding-a-new-cohort)

---

## 1. Understanding User Roles

Every account on the platform has one of four roles. Your role determines which pages you can access and what actions you can take.

| Role | Who It's For | Key Permissions |
|---|---|---|
| **User** | Newly registered accounts (default) | Very limited — waiting to be upgraded by a board member |
| **Intern** | Interns | Log hours, upload documents, complete assigned tasks |
| **Volunteer** | Volunteers | Same as Intern — log hours, upload documents, complete tasks, download grade reports and certificates |
| **Board** | Managers / administrators | Everything above, plus: create tasks, approve hours and documents, grade submissions, manage users |

> **Important:** When you first register, your role is set to **User**, which has very limited access. A board member must upgrade your role to **Intern** or **Volunteer** before you can use the platform fully. If you cannot see your dashboard or key menu items after logging in, contact a board member to have your role upgraded.

---

## 2. Getting Started — All Users

### 2.1 Registering an Account

1. Navigate to the platform's home page and click **Register** in the top navigation bar, or go directly to `/register`.
2. Fill in the registration form:
   - **Name** — your full name as you want it to appear on the platform
   - **Email** — your email address (must be unique; you will use this to log in)
   - **Password** — choose a secure password
   - **Confirm Password** — re-enter the same password
3. Click **Register**.
4. If there are any errors (e.g., the email is already in use, or passwords do not match), a red error message will appear directly under the relevant field. Fix the issue and try again.
5. On success, you will be redirected to the login page. Your account role is **User** by default — a board member will need to upgrade it.

---

### 2.2 Logging In

1. Navigate to `/login` or click **Login** in the navigation bar.
2. Enter your **Email** and **Password**.
   - Use the **eye icon** (👁) on the right side of the password field to show or hide your password as you type.
3. Click **Login**.
4. If your credentials are incorrect, an error message will appear below the form. Double-check your email and password and try again.
5. On success, you are redirected to your role-specific dashboard.

---

### 2.3 Editing Your Profile

1. Once logged in, go to **Edit Profile** (accessible from the navigation menu or at `/edit/profile`).
2. You can update the following:
   - **Name** — your display name across the platform
   - **Address** — your mailing or home address
   - **Profile Picture** — upload a photo (image file); this appears on your profile
3. Make your changes and click **Save** (or the equivalent submit button).
4. Changes take effect immediately.

> **Tip:** Filling out your address is important for certificate generation — it may be included in official documents.

---

### 2.4 Navigating Your Dashboard

After logging in, you are taken to your dashboard. What you see depends on your role:

**Volunteer/Intern Dashboard** (`/volunteer/dashboard` or `/intern/dashboard`)
- A welcome banner with your name
- Stats cards showing:
  - **Total Approved Hours** — hours logged and approved by a board member
  - **Total Activities** — number of individual hour logs submitted
  - **Projects Graded** — number of tasks that have been graded
- Quick links to your tasks and documents
- (Volunteers only) Quick access to download your **Grade Report** and **Service Certificate**

**Board Dashboard** (`/board/dashboard`)
- An overview of all users on the platform
- Quick links to pending hours, documents, and tasks requiring review
- Notification badges showing counts of items awaiting action

---

## 3. For Volunteers & Interns

### 3.1 Logging Hours

Use this section whenever you complete volunteer or intern work and need to record your time.

**How to log hours:**

1. Go to **Log Hours** in the navigation menu, or navigate to `/hours/log`.
2. Fill in the form:
   - **Activity Name** — a short, descriptive name for what you did (e.g., "Community Outreach Meeting")
   - **Date** — the date the activity took place
   - **Start Time** — the time you began
   - **End Time** — the time you finished (the platform automatically calculates the number of hours)
   - **Description** — a brief explanation of the activity and what you accomplished
3. Click **Submit**.

**What happens next:**

- Your submission appears under your hours history with a status of **Pending**.
- A board member reviews it and either **Approves** or **Denies** it.
- If approved, the hours are added to your **Total Hours** counter visible on your dashboard.
- If denied, the entry remains in your history marked as **Denied** and does not count toward your total.

**Viewing your hours history:**

- Navigate to `/specific/log/hours` to see all hours you have logged, along with their current status (Pending, Approved, or Denied).

---

### 3.2 Uploading Documents

Use this section to submit any onboarding paperwork or documents that have been requested from you.

**How to upload a document:**

1. Go to **Documents** in the navigation menu, or navigate to `/documents/status`.
2. This page shows all documents you have previously uploaded and their current status.
3. To upload a new document, use the upload form on this page:
   - **File** — select the file from your computer (accepted formats vary; check the form for guidance)
   - **Description** — describe what the document is (e.g., "Signed Volunteer Agreement")
4. Click **Upload** (or the equivalent submit button).

**What happens next:**

- Your document appears in your list with a status of **Pending**.
- A board member reviews it and either **Approves** or **Denies** it.
- You can check the status at any time by returning to `/documents/status`.

---

### 3.3 Managing Your Tasks

Tasks are assignments created by board members and assigned to you. Go to **My Tasks** in the navigation menu, or navigate to `/my/tasks`.

**The My Tasks page has three tabs:**

#### Tab 1: To Do
Shows all tasks currently assigned to you that you have not yet submitted. Tasks are automatically grouped into sections based on urgency:

| Section | Color | Meaning |
|---|---|---|
| **Past Due** | Red | The deadline has already passed — complete these immediately |
| **Due Today** | Yellow/Orange | Due by end of today |
| **Due This Week** | Blue | Due before the end of the current week |
| **Due Next Week** | Green | Due the following week |
| **Due Later** | Gray | Due more than two weeks out |

Each task card shows:
- The **task title** and a short preview of the description
- The **task type**: Project (blue header) or Reminder (blue-info header)
- The **due date**
- An **upload icon** (📤) if the task requires you to submit a file

Click **View & Complete** (or **View Details**) on any card to open the full task page.

#### Tab 2: Pending Review
Tasks you have already submitted but that have not yet been reviewed by a board member. No action is needed from you — just wait for the board to grade them.

#### Tab 3: Completed
Tasks that have been reviewed and graded. Each completed card shows:
- The task title
- Your **score**, if one was assigned (e.g., "85 / 100")
- A note if the board left feedback

---

### 3.4 Completing a Task

1. From the **To Do** tab on My Tasks, click **View & Complete** on the task you want to submit.
2. The task detail page opens showing:
   - The full task description
   - The due date (shown in red if overdue)
   - Whether a file upload is required
   - Who created the task
3. At the bottom of the page, you will see the **Mark as Complete** section.

**If the task requires a file upload:**
- A file upload field labeled **Upload File** will appear with a red asterisk (*) indicating it is required.
- Click the field and select your file from your computer. Accepted formats: PDF, DOC, DOCX, JPG, PNG.
- You cannot submit the task without attaching a file if this field is present.

**If the task does not require a file:**
- No upload field will appear.

**For all tasks:**
- Optionally fill in the **Completion Comments** text box — use this to explain what you did, add context, or ask questions for the reviewer.
- Click **Submit for Review**.

**What happens next:**
- The task moves to your **Pending Review** tab.
- A board member will review your submission and either grade it or send it back for revision.
- If sent back, the task returns to your **To Do** tab with the board's reason for the revision visible.

---

### 3.5 Viewing Your Grades

1. Navigate to `/grades/view` or use the **View Grades** link on your dashboard.
2. This page shows a formatted grade report listing all your graded tasks, including:
   - Task title
   - Score received (e.g., 85 / 100)
   - Feedback from the board member (if any was provided)
3. To download a PDF copy of your grades report, click **Download Grades** or navigate to `/grades/download`. The PDF will be generated and downloaded to your computer.

---

### 3.6 Downloading Your Certificate

Once you have accumulated hours and completed your assignments, you can download a service certificate.

1. Navigate to `/certificate/view` or click **View Certificate** on your dashboard.
2. The certificate is generated automatically and shows your name, total approved hours, and relevant details.
3. To save a copy, click **Download Certificate** or navigate to `/certificate/download`. This downloads the certificate as a PDF.

> **Note:** The certificate reflects your **total approved hours** at the time of download. If you log additional hours after downloading, re-download the certificate to get an updated version.

---

## 4. For Board Members

As a board member, you have access to everything volunteers and interns have, plus the ability to create and manage tasks, approve submissions, and manage users.

---

### 4.1 Approving Hours

When a volunteer or intern submits a hours log, it appears in your review queue.

1. Navigate to **Pending Hours** or go to `/pending/hours`.
2. You will see a list of all pending hour submissions, showing:
   - The **user's name and email**
   - **Activity name**
   - **Date** of the activity
   - **Start and end times**, and the **number of hours** calculated
   - **Description** provided by the user
3. For each entry, you have two options:
   - **Approve** — click the Approve button. The hours are added to the user's total approved hours and the entry is marked Approved.
   - **Deny** — click the Deny button. The entry is marked Denied and does not count toward the user's hours total.
4. The user can see the status update from their own hours history page.

---

### 4.2 Approving Documents

When a volunteer or intern uploads a document, it appears in your review queue.

1. Navigate to **Pending Documents** or go to `/pending/documents`.
2. You will see a list of all pending documents, showing:
   - The **user's name**
   - The **document description**
   - A link to **view the document**
3. Click the view link to open the document and review its contents.
4. For each document:
   - **Approve** — marks it as approved; the user can see the status change.
   - **Deny** — marks it as denied.

---

### 4.3 Creating an Assignment

Creating an assignment is a **two-step process**. Navigate to **Create Task** in the navigation menu or go to `/create/task`.

---

#### Step 1 of 2 — Task Details

Fill in the following fields:

**Title** *(required)*
A short, clear name for the task. Example: "Complete Volunteer Agreement Form"

**Description** *(required)*
Detailed instructions for what the user needs to do. Be specific — the person receiving this task sees exactly what you type here. Example: "Download the volunteer agreement from the shared drive, sign it, and upload a scanned copy."

**Classification** *(required)* — choose one:
- **Project** — use this for any substantive action item that requires the user to produce or complete something meaningful. Projects go through the grading workflow (submitted by the user → reviewed and graded by the board).
- **Reminder** — use this for notifications, check-ins, or lightweight recurring tasks. Reminders have extra options described below.

**Assigned Role** *(required)* — choose one:
- **Intern** — assigns the task to all users with the Intern role
- **Volunteer** — assigns the task to all users with the Volunteer role
- **Board** — assigns the task to all board members
- **Specific Users** — lets you hand-pick individual users in Step 2

---

**Reminder-Only Options** (only appear when Classification is set to Reminder):

**Make this a Recurring Reminder** *(checkbox)*
Check this box if you want the reminder to repeat automatically at a regular interval. When checked, two more fields appear:

- **Recurrence Frequency** — choose Daily, Weekly, Biweekly, or Monthly
- **Recurrence End Date** — the last date on which a new instance of this reminder should be generated

**Skip Review** *(checkbox)*
When checked, the reminder is automatically marked as complete the moment the user clicks "Submit for Review" — no board review or grading is required. Use this for simple acknowledgment reminders (e.g., "Check your email for the weekly update").

When Skip Review is **not** checked, the reminder follows the same review workflow as a project (submitted → board reviews → graded).

---

Click **Continue to Assignment Details** to proceed to Step 2.

---

#### Step 2 of 2 — Assignment Details

At the top of this page, you will see a summary confirming the task you just created (title, classification, assignment type, and any recurring or skip-review settings). Review this before continuing.

**Due Date** *(required)*
Enter the date by which the task must be completed. For recurring reminders, this is the due date for the **first occurrence** — subsequent occurrences are automatically generated based on the frequency you set.

**Upload Required** *(checkbox)*
Check this box if you want to require users to attach a file when submitting the task. When checked, users cannot submit the task without uploading a file. Leave unchecked if no file is needed.

**User Selection (only if you chose "Specific Users" in Step 1)**
A scrollable multi-select list of all users appears. Click each user you want to assign the task to. To select multiple users: hold **Ctrl** on Windows or **Cmd** on Mac while clicking.

**If you chose a role (not "Specific Users")**
A read-only list shows all users in that role who will receive the task. Review this list to confirm it looks correct.

---

Click **Assign Task to All [Role]s** (or **Assign Task to Selected Users** for specific assignments) to finalize.

The task is now created and assigned. Each user will see it appear in their **My Tasks → To Do** tab.

> **To cancel and start over:** Click the red **Cancel and Start Over** button at the bottom of Step 2. This permanently deletes the task you created in Step 1.

---

### 4.4 Grading a Task Submission

When a volunteer or intern submits a task, it enters the pending review queue.

**Option A — From the Pending Tasks list:**

1. Navigate to **Pending Tasks** or go to `/pending/tasks`.
2. This page shows a table of all submitted tasks awaiting review with the following columns:
   - **User** — name and email of the submitter
   - **Task** — title and brief description
   - **Type** — Project or Reminder badge
   - **Due Date** — original deadline (marked "Was Overdue" if submitted late)
   - **Upload** — a **View** button if the user attached a file, or "Not Required" / "Missing" if applicable
   - **Comments** — a **View** button if the user included completion comments (opens a popup with the full text)
   - **Actions** — a **Grade** button and a view icon
3. Click the **Grade** button for the task you want to review. A grading modal (popup) appears showing the user's name, task title, any submitted file, and any completion comments.
4. Fill in the grading fields:
   - **Score** *(optional)* — enter a numerator (e.g., 85)
   - **Denominator** *(optional)* — enter the total possible points (e.g., 100). Both together display as "85 / 100" for the user.
   - **Feedback** *(optional)* — written feedback visible to the user
5. Click **Submit Grade**. The task is marked as **Completed & Graded** and the user can see their score and feedback.

**Option B — From the task detail page:**

1. Navigate to `/pending/tasks` and click the eye icon (view icon) for a task, or find the task under **Tasks Status** at `/tasks/status`.
2. The task detail page shows the full description, the file preview (PDFs are rendered inline; images are displayed directly), and the user's comments.
3. Scroll to the bottom to find the **Grade This Task** section.
4. Fill in Score, Denominator, and Feedback as above.
5. Click **Submit Grade & Mark as Complete**.

---

### 4.5 Sending a Task Back for Revision

If a submission is insufficient and needs to be redone, you can return it to the user instead of grading it.

1. Open the task detail page for a pending submission (from `/pending/tasks`, click the eye/view icon).
2. Scroll to the bottom. Below the grading form, you will see a **Send Back for Revision** section.
3. Fill in:
   - **New Due Date** *(optional)* — pre-filled with the original due date; change it if you want to give the user more time
   - **Reason** *(optional but recommended)* — explain what was wrong and what the user needs to fix
4. Click **Send Back to Student**.
5. The task returns to the user's **To Do** tab with status reset to pending. The reason you wrote is visible to the user when they open the task.

---

### 4.6 Managing Users

Navigate to **User List** in the navigation menu or go to `/user/list`.

#### Searching and Filtering Users
- Use the **search bar** to filter by name.
- Use the **role filter** dropdown to show only users with a specific role.
- The list updates as you type/select.

#### Viewing a User's Details
Click on a user's name or row to see their individual records:
- **Hours** — their full hours log history at `/specific/log/hours`
- **Documents** — their uploaded documents
- **Tasks** — all tasks assigned to them and their statuses

#### Upgrading a User's Role
1. Navigate to `/upgrade/user`.
2. Select the user from the dropdown.
3. Select the new role you want to assign them (User, Intern, Volunteer, or Board).
4. Click **Upgrade** (or the equivalent submit button).
5. The user will see their new dashboard and permissions immediately on their next page load.

> **Typical flow:** A new registrant comes in as **User** → you upgrade them to **Intern** or **Volunteer** so they can access their dashboard, log hours, and complete tasks.

#### Deleting a User
1. Navigate to `/delete/user`.
2. Select the user from the dropdown.
3. Confirm the deletion.

> **Warning:** Deleting a user is permanent. All of their hours, documents, and task assignments are also deleted. Double-check before proceeding.

---

### 4.7 Activity Log & Notifications

**Notifications badge:** The navigation bar shows a notification badge with counts of items awaiting your action (e.g., pending hours, pending documents, pending task reviews). Use these as a quick indicator of what needs attention.

**Activity Log:**
1. Navigate to **Notifications** or go to `/notification`.
2. This page shows a chronological log of all significant actions taken on the platform, including:
   - User role changes (who upgraded whom)
   - Task grades submitted (who graded which user's task)
   - Document uploads and approvals
   - Hour log approvals and denials
3. Each entry shows: **who** performed the action, **what** the action was, **what/whom** it affected, and **when** it happened.

Use the activity log to audit actions, resolve disputes, or simply keep track of what has happened across the platform.

---

## 5. Common End-to-End Workflows

### 5.1 New Volunteer Getting Started

This is the expected flow for someone who has just joined the organization.

1. **Register** at `/register` — fill in your name, email, and password.
2. **Contact a board member** and ask them to upgrade your role from **User** to **Volunteer** (or Intern).
3. **Log in** at `/login`.
4. **Edit your profile** at `/edit/profile` — add your address and a profile photo.
5. **Check My Tasks** at `/my/tasks` — see if any tasks have already been assigned to you.
6. **Log your first hours** at `/hours/log` after completing any volunteer activity.
7. **Upload any required documents** at `/documents/status` if your coordinator has asked for paperwork.
8. **Complete assigned tasks** by opening them from My Tasks, following the instructions, attaching a file if required, and clicking Submit for Review.
9. **Check back for grades** — completed tasks appear in the Completed tab with any scores and feedback.
10. **Download your certificate** at `/certificate/download` once you have accumulated approved hours.

---

### 5.2 Board Onboarding a New Cohort

This is the expected flow when a board member is setting up the platform for a new group of volunteers or interns.

1. **Verify new registrants** — go to `/user/list`, find users with the **User** role, and upgrade each one to **Intern** or **Volunteer** at `/upgrade/user`.
2. **Create onboarding tasks** — go to `/create/task` and build the assignments the cohort needs to complete:
   - For each task, decide: Is this a Project (graded) or a Reminder (acknowledgment)?
   - Set the Assigned Role to **Intern** or **Volunteer** to assign to all members of that group at once.
   - Set the Due Date for the first deadline.
   - Check **Upload Required** for any tasks that require document submission.
3. **Create recurring reminders** (if needed) — for regular check-ins (e.g., weekly hour-logging reminders), create a Reminder with **Make this a Recurring Reminder** checked, set the frequency and end date, and optionally check **Skip Review** if no grading is needed.
4. **Monitor pending queues** — as cohort members submit work, review them from:
   - `/pending/hours` for hour log approvals
   - `/pending/documents` for document approvals
   - `/pending/tasks` for task submissions awaiting grading
5. **Grade submissions** — for each pending task, review the user's file and comments, enter a score and feedback, and click Submit Grade.
6. **Send back revisions as needed** — if a submission is incomplete, use the Send Back for Revision form with a clear explanation of what to fix.
7. **Track activity** — use the activity log at `/notification` to monitor all platform actions.

---

*If you encounter any issues or have questions not covered in this guide, reach out to your platform administrator or a board member.*
