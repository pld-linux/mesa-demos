#
# Conditional build:
%bcond_without	egl	# EGL utilities
%bcond_without	gles1	# GLESv1 utilities
%bcond_without	gles2	# GLESv2 utilities
%bcond_with	openvg	# OpenVG utilities
%bcond_without	wayland	# Wayland support

Summary:	Mesa Demos source code
Summary(pl.UTF-8):	Kod źródłowy programów demonstrujących dla bibliotek Mesa
Name:		mesa-demos
Version:	8.3.0
Release:	1
License:	various (MIT, SGI, GPL - see copyright notes in sources)
Group:		Development/Libraries
Source0:	ftp://ftp.freedesktop.org/pub/mesa/demos/%{version}/%{name}-%{version}.tar.bz2
# Source0-md5:	628e75c23c17394f11a316c36f8e4164
URL:		http://www.mesa3d.org/
%{?with_egl:BuildRequires:	EGL-devel}
BuildRequires:	Mesa-libgbm-devel
%{?with_wayland:BuildRequires:	Mesa-libwayland-egl-devel}
BuildRequires:	OpenGL-GLU-devel
BuildRequires:	OpenGL-devel
BuildRequires:	OpenGL-glut-devel
%{?with_gles1:BuildRequires:	OpenGLESv1-devel}
%{?with_gles2:BuildRequires:	OpenGLESv2-devel}
%{?with_openvg:BuildRequires:	OpenVG-devel}
BuildRequires:	freetype-devel >= 2
BuildRequires:	glew-devel >= 1.5.4
%{?with_egl:BuildRequires:	libdrm-devel}
BuildRequires:	pkgconfig
BuildRequires:	rpm-pythonprov
%{?with_wayland:BuildRequires:	wayland-devel}
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-lib-libXext-devel
Requires:	OpenGL-devel
Requires:	OpenGL-glut-devel
Obsoletes:	Mesa-demos
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Demonstration programs for the Mesa libraries in source code form.

%description -l pl.UTF-8
Kod źródłowy programów demonstracyjnych dla bibliotek Mesa.

%package -n mesa-utils
Summary:	OpenGL utilities from Mesa3D
Summary(pl.UTF-8):	Programy narzędziowe OpenGL z projektu Mesa3D
License:	MIT
Group:		X11/Applications/Graphics
Obsoletes:	Mesa-utils

%description -n mesa-utils
OpenGL utilities from Mesa3D: glxgears and glxinfo.

%description -n mesa-utils -l pl.UTF-8
Programy narzędziowe OpenGL z projektu Mesa3D: glxgears i glxinfo.

%package -n mesa-utils-egl
Summary:	EGL utilities from Mesa3D
Summary(pl.UTF-8):	Programy narzędziowe EGL z projektu Mesa3D
License:	MIT
Group:		Applications/Graphics

%description -n mesa-utils-egl
EGL utilities from Mesa3D: eglgears and eglinfo.

%description -n mesa-utils-egl -l pl.UTF-8
Programy narzędziowe EGL z projektu Mesa3D: eglgears i eglinfo.

%package -n mesa-utils-gles1
Summary:	OpenGLESv1 utilities from Mesa3D
Summary(pl.UTF-8):	Programy narzędziowe OpenGLESv1 z projektu Mesa3D
License:	MIT
Group:		Applications/Graphics

%description -n mesa-utils-gles1
OpenGLESv1 utilities from Mesa3D: es1gears and es1_info.

%description -n mesa-utils-gles1 -l pl.UTF-8
Programy narzędziowe OpenGLESv1 z projektu Mesa3D: es1gears i
es1_info.

%package -n mesa-utils-gles2
Summary:	OpenGLESv2 utilities from Mesa3D
Summary(pl.UTF-8):	Programy narzędziowe OpenGLESv2 z projektu Mesa3D
License:	MIT
Group:		Applications/Graphics

%description -n mesa-utils-gles2
OpenGLESv2 utilities from Mesa3D: es2gears and es2_info.

%description -n mesa-utils-gles2 -l pl.UTF-8
Programy narzędziowe OpenGLESv2 z projektu Mesa3D: es2gears i
es2_info.

%package -n mesa-utils-openvg
Summary:	OpenVG utilities from Mesa3D
Summary(pl.UTF-8):	Programy narzędziowe OpenVG z projektu Mesa3D
License:	MIT
Group:		Applications/Graphics

%description -n mesa-utils-openvg
OpenVG utilities from Mesa3D.

%description -n mesa-utils-openvg -l pl.UTF-8
Programy narzędziowe OpenVG z projektu Mesa3D.

%prep
%setup -q

%build
%configure \
	%{!?with_egl:--disable-egl} \
	%{!?with_gles1:--disable-gles1} \
	%{!?with_gles2:--disable-gles2} \
	--disable-silent-rules \
	%{!?with_openvg:--disable-vg} \
	%{?with_egl:--enable-wayland}

# we only want glxinfo and glxgears to be built here
%{__make} -C src/xdemos

%if %{with egl}
%{__make} -C src/egl
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_examplesdir}/%{name}-%{version}}

install -p src/xdemos/{glxinfo,glxgears} $RPM_BUILD_ROOT%{_bindir}
%if %{with egl}
install -p src/egl/opengl/{eglinfo,eglgears_x11,peglgears} $RPM_BUILD_ROOT%{_bindir}
%if %{with gles1}
install -p src/egl/opengles1/es1_info $RPM_BUILD_ROOT%{_bindir}
install -p src/egl/opengles1/gears_x11 $RPM_BUILD_ROOT%{_bindir}/es1gears_x11
%endif
%if %{with gles2}
install -p src/egl/opengles2/{es2_info,es2gears_x11} $RPM_BUILD_ROOT%{_bindir}
%if %{with wayland}
install -p src/egl/opengles2/es2gears_wayland $RPM_BUILD_ROOT%{_bindir}
%endif
%endif
%if %{with openvg}
install -p src/egl/openvg/{lion,sp}_x11 $RPM_BUILD_ROOT%{_bindir}
%endif
%endif

cp -a * $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
%{__make} -C $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version} distclean

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%{_examplesdir}/%{name}-%{version}

%files -n mesa-utils
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/glxgears
%attr(755,root,root) %{_bindir}/glxinfo

%if %{with egl}
%files -n mesa-utils-egl
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/eglgears_x11
%attr(755,root,root) %{_bindir}/eglinfo
%attr(755,root,root) %{_bindir}/peglgears
%endif

%if %{with egl} && %{with gles1}
%files -n mesa-utils-gles1
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/es1_info
%attr(755,root,root) %{_bindir}/es1gears_x11
%endif

%if %{with egl} && %{with gles2}
%files -n mesa-utils-gles2
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/es2_info
%attr(755,root,root) %{_bindir}/es2gears_x11
%if %{with wayland}
%attr(755,root,root) %{_bindir}/es2gears_wayland
%endif
%endif

%if %{with egl} && %{with openvg}
%files -n mesa-utils-openvg
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/lion_x11
%attr(755,root,root) %{_bindir}/sp_x11
%endif
