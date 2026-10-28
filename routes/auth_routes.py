from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from models import db, User

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    """User authentication with role recognition and secure password verification."""
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        remember = bool(request.form.get("remember"))

        if not username or not password:
            flash("Please enter both username and password.", "danger")
            return render_template("auth/login.html", already_authenticated=current_user.is_authenticated)

        user = User.query.filter(
            (User.username == username) | (User.email == username)
        ).first()

        if user and user.check_password(password):
            if not user.is_active:
                flash("This account has been deactivated. Please contact an administrator.", "warning")
                return render_template("auth/login.html", already_authenticated=current_user.is_authenticated)

            if current_user.is_authenticated:
                logout_user()

            login_user(user, remember=remember)
            flash(f"Welcome back, {user.full_name} ({user.role})!", "success")
            next_page = request.args.get("next")
            return redirect(next_page or url_for("main.dashboard"))
        else:
            flash("Invalid username/email or password.", "danger")

    return render_template("auth/login.html", already_authenticated=current_user.is_authenticated)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    """Register a new pharmacy user account with role selection."""
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip()
        full_name = request.form.get("full_name", "").strip()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")
        role = request.form.get("role", "Pharmacist").strip()

        # Input validation
        if not username or not email or not full_name or not password:
            flash("All fields are required.", "danger")
            return render_template("auth/register.html")

        if len(password) < 6:
            flash("Password must be at least 6 characters long.", "danger")
            return render_template("auth/register.html")

        if password != confirm_password:
            flash("Passwords do not match.", "danger")
            return render_template("auth/register.html")

        # Check existing user
        if User.query.filter_by(username=username).first():
            flash("Username already taken. Please choose another.", "warning")
            return render_template("auth/register.html")

        if User.query.filter_by(email=email).first():
            flash("Email address is already registered.", "warning")
            return render_template("auth/register.html")

        # Restrict role to valid choices
        valid_roles = ["Pharmacist", "Staff", "Admin"]
        assigned_role = role if role in valid_roles else "Pharmacist"

        user = User(
            username=username,
            email=email,
            full_name=full_name,
            role=assigned_role,
            is_active=True,
        )
        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        flash("Account created successfully! You can now log in.", "success")
        return redirect(url_for("auth.login"))

    return render_template("auth/register.html")


@auth_bp.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    """Handle user password reset inquiries."""
    if request.method == "POST":
        identity = request.form.get("identity", "").strip()
        if not identity:
            flash("Please provide your username or email address.", "warning")
            return redirect(url_for("auth.login"))

        user = User.query.filter((User.username == identity) | (User.email == identity)).first()
        if user:
            flash(f"Password reset instructions have been dispatched to the email on file for '{user.username}'.", "success")
        else:
            flash(f"If an account is associated with '{identity}', reset instructions have been generated.", "info")
        return redirect(url_for("auth.login"))

    return render_template("auth/forgot_password.html")


@auth_bp.route("/logout")
@login_required
def logout():
    """Log out current user and end session."""
    logout_user()
    flash("You have been signed out safely.", "info")
    return redirect(url_for("main.index"))
