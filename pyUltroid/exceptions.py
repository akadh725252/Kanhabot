# kanha - UserBot
# Copyright (C) 2021-2023 Teamkanha
#
# This file is a part of < https://github.com/Teamkanha/kanha/ >
# PLease read the GNU Affero General Public License in
# <https://github.com/Teamkanha/pykanha/blob/main/LICENSE>.

"""
Exceptions which can be raised by py-kanha Itself.
"""


class pykanhaError(Exception):
    ...


class DependencyMissingError(ImportError):
    ...


class RunningAsFunctionLibError(pykanhaError):
    ...
