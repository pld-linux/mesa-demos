#
# Conditional build:
%bcond_without	egl	# EGL utilities
%bcond_without	gles1	# GLESv1 utilities
%bcond_without	gles2	# GLESv2 utilities
%bcond_without	wayland	# Wayland support

Summary:	Mesa Demos source code
Summary(pl.UTF-8):	Kod źródłowy programów demonstrujących dla bibliotek Mesa
Name:		mesa-demos
Version:	9.0.0
Release:	1
License:	various (MIT, SGI, GPL - see copyright notes in sources)
Group:		Development/Libraries
Source0:	https://archive.mesa3d.org/demos/%{name}-%{version}.tar.xz
# Source0-md5:	bd63d3d5b898851f09d87d6537843320
URL:		https://www.mesa3d.org/
%{?with_egl:BuildRequires:	EGL-devel}
BuildRequires:	Mesa-libgbm-devel
BuildRequires:	OpenGL-GLU-devel
BuildRequires:	OpenGL-devel
BuildRequires:	OpenGL-glut-devel
%{?with_gles1:BuildRequires:	OpenGLESv1-devel}
%{?with_gles2:BuildRequires:	OpenGLESv2-devel}
BuildRequires:	freetype-devel >= 2
BuildRequires:	glew-devel >= 1.5.4
%{?with_wayland:BuildRequires:	libdecor-devel >= 0.1}
BuildRequires:	libstdc++-devel >= 6:7
%{?with_egl:BuildRequires:	libdrm-devel}
BuildRequires:	meson >= 0.59
BuildRequires:	ninja >= 1.5
BuildRequires:	pkgconfig
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRequires:	sed >= 4.0
BuildRequires:	tar >= 1:1.22
%{?with_wayland:BuildRequires:	wayland-devel}
%{?with_wayland:BuildRequires:	wayland-egl-devel}
%{?with_wayland:BuildRequires:	wayland-protocols >= 1.12}
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-lib-libXext-devel
%{?with_wayland:BuildRequires:	xorg-lib-libxkbcommon-devel}
BuildRequires:	xz
Requires:	OpenGL-devel
Requires:	OpenGL-glut-devel
Obsoletes:	Mesa-demos < 7.9
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
Obsoletes:	Mesa-utils < 7.9
Obsoletes:	Mesa-utils-openvg < 8.5

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

%prep
%setup -q

%{__sed} -i -e '1s,/usr/bin/env python2,%{__python},' src/tests/api_speed.py

%build
%meson build \
	%{!?with_egl:-Degl=disabled} \
	%{!?with_gles1:-Dgles1=disabled} \
	%{!?with_gles2:-Dgles2=disabled} \
	-Dglut=disabled \
	-Dlibdrm=disabled \
	-Dosmesa=disabled \
	-Dvulkan=disabled \
	%{!?with_wayland:-Dwayland=disabled} \
	-Dwith-system-data-files=true

%ninja_build -C build

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_examplesdir}/%{name}-%{version}}

install -p build/src/xdemos/{glxinfo,glxgears} $RPM_BUILD_ROOT%{_bindir}
%if %{with egl}
install -p build/src/egl/opengl/{eglinfo,eglgears_x11,peglgears} $RPM_BUILD_ROOT%{_bindir}
%if %{with gles1}
install -p build/src/egl/opengles1/es1_info $RPM_BUILD_ROOT%{_bindir}
install -p build/src/egl/opengles1/gears_x11 $RPM_BUILD_ROOT%{_bindir}/es1gears_x11
%endif
%if %{with gles2}
install -p build/src/egl/opengles2/{es2_info,es2gears_x11} $RPM_BUILD_ROOT%{_bindir}
%if %{with wayland}
install -p build/src/egl/opengles2/es2gears_wayland $RPM_BUILD_ROOT%{_bindir}
%endif
%endif
%endif

cp -a meson* src $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

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
