Summary:	A graphical user interface for the Argyll CMS display calibration utilities
Name:		dispcalGUI
Version:	0.7.8.9
Release:	19.6
License:	GPL v3
Source0:	http://dispcalGUI.hoech.net/%{name}-%{version}.tar.gz
# Source0-md5:	0b26561e61761e6be99964b35496af41
Group:		Applications/Multimedia
URL:		http://dispcalgui.hoech.net/
BuildRequires:	desktop-file-utils
BuildRequires:	python-devel
BuildRequires:	udev-core
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-lib-libXinerama-devel
BuildRequires:	xorg-lib-libXrandr-devel
BuildRequires:	xorg-lib-libXxf86vm-devel
Requires:	desktop-file-utils
Requires:	gtk-update-icon-cache
Requires:	hicolor-icon-theme
Requires:	python-numpy >= 1.0
Requires:	python-wxPython >= 2.8.6
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Calibrates and characterizes display devices using a hardware sensor,
driven by the open source color management system Argyll CMS. Supports
multi-display setups and a variety of available settings like
customizable whitepoint, luminance, black level, tone response curve
as well as the creation of matrix and look-up-table ICC profiles with
optional gamut mapping. Calibrations and profiles can be verified
through measurements, and profiles can be installed to make them
available to color management aware applications. Profile installation
can utilize Argyll CMS, Oyranos and/or GNOME Color Manager if
available, for flexible integration.

%prep
%setup -q
# Make files executable
chmod +x scripts/*
chmod +x misc/Argyll

find -name .DS_Store | xargs rm -rv

%build
%{__python} setup.py build --use-distutils

%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install \
	--optimize=2 \
	--skip-build \
	--skip-instrument-configuration-files \
	--skip-postinstall \
	--use-distutils \
	--prefix=%{_prefix} \
	--root=$RPM_BUILD_ROOT \

#%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/%{name}/tests

%py_postclean

install -d $RPM_BUILD_ROOT/lib/udev/rules.d
cp -p misc/92-Argyll.rules $RPM_BUILD_ROOT/lib/udev/rules.d

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_desktop_database_post
%update_icon_cache hicolor

%postun
%update_desktop_database_postun
%update_icon_cache hicolor

%files
%defattr(644,root,root,755)
%doc README.html screenshots theme
/etc/xdg/autostart/z-dispcalGUI-apply-profiles.desktop
/lib/udev/rules.d/92-Argyll.rules
%attr(755,root,root) %{_bindir}/dispcalGUI
%attr(755,root,root) %{_bindir}/dispcalGUI-apply-profiles
%{_mandir}/man1/dispcalGUI-apply-profiles.1*
%{_mandir}/man1/dispcalGUI.1*
%{_desktopdir}/dispcalGUI.desktop
%{_iconsdir}/hicolor/*/apps/dispcalGUI.png

%dir %{py_sitedir}/%{name}
%{py_sitedir}/%{name}/*.py[co]
%{py_sitedir}/%{name}-*.egg-info
%dir %{py_sitedir}/%{name}/%{_lib}
%{py_sitedir}/%{name}/%{_lib}/*.py[co]
%dir %{py_sitedir}/%{name}/%{_lib}/python*
%{py_sitedir}/%{name}/%{_lib}/python*/*.py[co]
%attr(755,root,root) %{py_sitedir}/%{name}/%{_lib}/python*/RealDisplaySizeMM.so

%dir %{_datadir}/%{name}
%{_datadir}/%{name}/*.json
%{_datadir}/%{name}/test.cal
%{_datadir}/%{name}/pnp.ids
%{_datadir}/%{name}/presets
%{_datadir}/%{name}/ref
%{_datadir}/%{name}/report
%{_datadir}/%{name}/tests
%{_datadir}/%{name}/theme
%{_datadir}/%{name}/ti1
%{_datadir}/%{name}/xrc
%dir %{_datadir}/%{name}/lang
%{_datadir}/%{name}/lang/en.json
%lang(de) %{_datadir}/%{name}/lang/de.json
%lang(es) %{_datadir}/%{name}/lang/es.json
%lang(fr) %{_datadir}/%{name}/lang/fr.json
%lang(it) %{_datadir}/%{name}/lang/it.json
