#						-*- Autoconf -*-
# Process this file with autoconf to produce a configure script.

AC_INIT([scribes], [0.4-eurika-dev-build409], [<mystilleef@gmail.com>])
GNOME_COMMON_INIT
AC_PREREQ(2.60)
AM_INIT_AUTOMAKE([1.8 dist-bzip2 no-dist-gzip])
AM_MAINTAINER_MODE

AC_CONFIG_MACRO_DIR([m4])
AC_CONFIG_SRCDIR([configure.ac])
AC_PREFIX_DEFAULT([/usr])
IT_PROG_INTLTOOL([0.35.0])

dnl ================================================================
dnl Gettext stuff.
dnl ================================================================

GETTEXT_PACKAGE=scribes
AC_SUBST(GETTEXT_PACKAGE)
AC_DEFINE_UNQUOTED(GETTEXT_PACKAGE,"$GETTEXT_PACKAGE", [Gettext package])
ALL_LINGUAS="de fr nl it pt_BR sv zh_CN"
AM_GLIB_GNU_GETTEXT

# Checks for programs.
AC_PATH_PROG([SED], [sed])
#AC_PATH_PROG([GCONFTOOL], [gconftool-2])
AC_PATH_PROG([YELP], [yelp])
GNOME_DOC_INIT
#AM_GCONF_SOURCE_2

AM_PATH_PYTHON([2.5])
AC_LANG([C])
AC_RUN_IFELSE([AC_LANG_PROGRAM([[#include <stdlib.h>]],[[int result = system("python depcheck.py"); if (result != 0) exit(EXIT_FAILURE);]])], [], [AC_MSG_ERROR([Error: Dependency check failed])])

AC_CONFIG_FILES([
po/Makefile.in
Makefile
help/Makefile
SCRIBES/Makefile
SCRIBES/URILoader/Makefile
SCRIBES/GUI/Makefile
SCRIBES/GUI/MainGUI/Makefile
SCRIBES/GUI/MainGUI/StatusBar/Makefile
SCRIBES/GUI/MainGUI/Window/Makefile
SCRIBES/GUI/MainGUI/Toolbar/Makefile
SCRIBES/GUI/MainGUI/View/Makefile
SCRIBES/GUI/MainGUI/View/DatabaseListeners/Makefile
SCRIBES/GUI/MainGUI/Buffer/Makefile
data/Makefile]
)

AC_OUTPUT
