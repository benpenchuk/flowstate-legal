---
title: FlowState Privacy Policy
---

# FlowState — Privacy Policy

**Last updated:** 10 October 2026

## Who and what

FlowState is a workout tracker for iPhone, made by Ben Penchuk, an individual. In this policy "we" means him. It says what FlowState collects, where that goes, and how to get rid of it.

## The short version

- **An account is required.** Your training is saved on your phone first and backed up to your account, so a new phone can restore it. That backup is the only one. FlowState has no export feature.
- **No ads, no analytics SDK, no tracking.** Nothing is sold, and nothing is shared for anyone else's use.
- **You can delete everything from inside the app, at any time.** Delete account erases your account, its backup on our server, and the workouts, templates, records and weigh-ins on that iPhone. It cannot be undone.

## What we collect

All of this is stored on your phone. Once you are signed in, it is also backed up to your account.

- **Account:** your email address (Apple's relay address if you hide yours when you use Sign in with Apple), how you signed in (Apple or email), your account ID, and a username if your account has one. If you sign up with email, your password is held by our sign-in service, not by us in readable form.
- **Profile, all optional:** first name, last name and display name (Sign in with Apple can supply your name), a contact email, **phone number**, **birth date**, **gender** and **height**.
- **Profile picture:** one of eight preset pictures, or your initials. FlowState never asks for, reads or uploads a photo.
- **Settings and goals:** units, default rest time, appearance, training goal, experience level, days per week and the equipment you have. A few switches, such as the rest alert sound, stay on the phone only.
- **Training:** workouts (name, start and finish times, notes, effort rating, total rest time and total volume), the exercises in them, and every set (weight, reps, duration, distance, equipment, set type, reps in reserve or RPE, notes, and when it was done). Also templates, custom exercises you create, and which exercises you favourite or hide. Anything you type into a name or a note is saved too. Personal records are worked out on your phone from your sets and are not stored separately on our server.
- **Body:** weigh-ins and body-fat percentages you enter, and body weights imported from Apple Health (see Apple Health below).
- **App state:** which onboarding steps you have finished, so a restore does not ask you again.
- **Server logs:** our host keeps ordinary request logs, which include your IP address, for a short time to run and secure the service. We do not use them to profile you.

Gender, phone number, birth date and height are optional. No feature calculates anything from them today. They are stored with your profile.

## What we don't collect

- Location, contacts, photos, microphone, or advertising identifiers.
- Analytics or behavioural tracking. FlowState contains no advertising or analytics SDK. The app's only network connections are to our backend and, for Sign in with Apple, to Apple.
- Crash reports. iOS gives the app daily crash and performance reports (Apple's MetricKit), and the app writes its own error messages next to them in a log file on your phone. FlowState never uploads that log. Feedback includes only its recent backup (sync) messages, as described below. Deleting the app removes it. Delete account does not.
- Separately, if you have turned on "Share With App Developers" in iOS settings, Apple may send us anonymous crash reports. Those come from Apple, not from the app.
- Feedback: Settings → Send feedback opens your own mail app with a message addressed to us. It is prefilled with a short technical summary to help us fix backup problems: the app version, iOS version, device model, backup status, how many changes are waiting to back up, when the last backup worked, and recent backup error messages. It contains no workouts, sets, notes or profile details. You can read, edit or delete the summary before sending. We receive only what you send, from the email account you send it from.

## How it's used

Only to run the app: show your history, back it up, and restore it on a new phone. It is never used for advertising, never sold, and never used to train AI models.

## Where it's stored

- **On your phone**, in the app's own storage. FlowState does not use iCloud to sync.
- **In Supabase**, which hosts our database and sign-in. The project is in the US East (Ohio) region, so if you are outside the United States your data is sent to the United States. Supabase acts as our processor.
- Every table is protected by row-level security, so other FlowState users cannot read your rows. As the operator, we can reach the database through Supabase's admin tools.
- Apple handles Sign in with Apple under its own privacy policy.

## Apple Health

Apple Health access is optional and only with your permission. FlowState asks once, in one sheet, for both of the things below.

- **Writing:** FlowState saves each finished workout to Health as a strength-training workout. It writes the start and end time and FlowState's internal ID for the workout. It does not write sets, reps, weights or notes.
- **Reading:** FlowState reads your body weight from Health each time you open the app. The first import looks back one year. **Each weight it reads is saved in FlowState as a weigh-in and backed up to your account, like a weight you type.**
- Health data is never used for advertising or marketing, never sold, and never shared with anyone other than our backend host, which stores the imported weights for us as described above.
- To stop new reads and writes, turn off FlowState's access in Settings → Privacy & Security → Health → FlowState. Weights already imported stay in FlowState until you delete them there or delete your account. Deleting a weight in the Health app does not remove FlowState's copy.
- Delete account does not remove workouts FlowState saved to Health. You can delete those in the Health app.

## Retention

- Your data is kept while your account exists.
- When you delete a workout, an exercise in a workout, a set, a template, a custom exercise or a weigh-in, the server does not remove the row. It marks it as deleted (a deletion marker, sometimes called a tombstone) so your other devices delete it too. **Today that marker can still hold what the row held**, such as a set's weight and reps or a workout's name, times and notes, until you delete your account.
- When you delete your account, your rows leave the server straight away. Copies can remain in backups for up to 30 days: Supabase's routine daily backups last 7 days, and any backup we take ourselves is deleted within 30 days.
- Server logs are kept for a short time and then removed.

## Your controls

- **Sign out:** your data stays on the phone and in your account. You sign in again to keep using FlowState.
- **Delete account** (Settings, at the bottom, when you are signed in): permanently erases your account and its backup on our server, and the workouts, templates, records, custom exercises and weigh-ins on that iPhone. It also clears the name, username, birth date, gender, height, email, phone number, goal, experience and days per week from the phone. Only app preferences such as units and appearance stay. It needs an internet connection, and if the server cannot delete your account nothing is changed. It does not remove FlowState from your Apple ID's Sign in with Apple list. You can do that in iOS Settings → your name → Sign-In & Security → Sign in with Apple.
- **Delete the app:** removes the copy on the phone. Your account and its backup remain, and signing in again restores them.
- **Share a workout:** the share button on a workout sends a text summary of that one workout to the app you pick. FlowState has no way to export everything.
- **Access, correction, a copy of your data, or deletion by request:** email the address under Contact and we will reply within 30 days. This covers your rights under GDPR, UK GDPR, the California CCPA, and Washington and Nevada consumer health data law. If we refuse a request, you can appeal by replying to our answer. FlowState does not sell or share personal data, so there is nothing to opt out of.

## Consumer health data

For Washington's My Health My Data Act and Nevada's consumer health data law, this is the health-related data FlowState handles.

| Data | Where it comes from | Why | Who gets it |
|---|---|---|---|
| Body weight and body-fat percentage | You, or Apple Health (weight only) | Show your weigh-ins and back them up | Supabase, as our processor |
| Height, birth date, gender (optional) | You | Stored with your profile | Supabase, as our processor |
| Workouts, sets, exercises, effort and goals | You, using the app | Show your history and back it up | Supabase, as our processor |

We do not sell this data and we do not share it with anyone else. You can withdraw consent by turning off Health access, or by deleting your account. You can ask us to delete it, or to tell you what we hold, using the address under Contact.

## Security

- Data is encrypted in transit (TLS).
- Your sign-in session is kept in your iPhone's Keychain.
- If a breach affects your data, we will tell you.

## Age

FlowState is not for children under 13, and we do not knowingly collect their data. Where the age of digital consent is higher (up to 16 in parts of the EU), you need a parent's permission. If you think a child has an account, contact us and we will delete it.

## Changes

We will update the date at the top. If a change is material, we will tell you before it takes effect, by email to the address on your account.

## Contact

Questions, requests and feedback: {{contact}}
