# coding=utf8
#
# Copyright (C) 2011  Edmundo Álvarez Jiménez
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Authors: Edmundo Álvarez Jiménez <e.alvarezj@gmail.com>

class UserMsgs:
    
    # Success messages
    APP_ADDED = "Nice! Thanks to you we have a new application to discover."
    APP_EDITED = "Application has been edited. Thanks for keep us updated."
    COMMENT_ADDED = "Thanks for your comment!"
    USER_CREATED = "Thank you for joining! Your profile has been created."
    USER_EDITED = "Don't you feel something has changed? Your profile " + \
            "has been edited."
    FRIEND_ADDED = "Whoa! You have a new friend ;-)"
    FRIEND_REMOVED = "You have lost a friend :-("
    CHECKAPP_DONE = "Great! Thanks for checking app!"
    MERIT_ACHIEVED = "Congratulations! You have achieved a new merit."
    
    # Warning messages
    FORM_ERROR = "There are some errors on your data:"
    LIMITED_VIEW = "You can't fully enjoy CheckApp if you don't login."
    CHECKAPPS_EXCEEDED = "Sorry, you have made your five check-apps today :-("
    
    # Error messages
    LOGIN = "Please login or create an account to access CheckApp." 
    LOGIN_ERROR = "Invalid username or password."
    DISABLED_ACCOUNT = "Your account is disabled. What have you done? " + \
            "Please contact us for more information."
    FORBIDDEN = "You don't have permissions to access this page."
    UNEXPECTED_ERROR = "Oops! Something wrong has happened. Please try again."

