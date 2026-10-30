Name:           waywallen-flatpak
Version:        1.0
Release:        1%{?dist}
Summary:        RPM wrapper to help install and run waywallen Flatpak
License:        MIT
BuildArch:      noarch

Conflicts:      waywallen
Requires:       bash
Requires:       flatpak

%define debug_package %{nil}

%description
A helper package that ensures Flathub is enabled, helps with install waywallen Flatpak, and provides a command-line launcher for waywallen.

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_bindir}

cat << 'INNER_EOF' > %{buildroot}%{_bindir}/waywallen
#!/bin/bash
if ! command -v flatpak &> /dev/null; then
  echo "Error: Flatpak is not installed."
  echo "Install it via running: dnf install flatpak"
  exit 1
else
  if ! flatpak list --app | grep -q "org.waywallen.waywallen"; then
    if ! flatpak remotes | grep -q "flathub"; then
      echo "Error: Flathub flatpak repo not found."
      echo "Please check for install guide: https://flathub.org/setup/Fedora" 
      exit 1
    else
    echo "Error: waywallen flatpak not found."
    echo "Please run: flatpak install flathub org.waywallen.waywallen"
    exit 1
    fi
  fi
fi
exec flatpak run org.waywallen.waywallen "$@"
INNER_EOF

chmod +x %{buildroot}%{_bindir}/waywallen

%files
%{_bindir}/waywallen

%changelog
* Wed Oct 07 2026 L1oly <https://github.com/L1oly> - 1.0-1
- Initial release
