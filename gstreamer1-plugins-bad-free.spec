%global         majorminor 1.0
%bcond_with extras

Name:           gstreamer1-plugins-bad-free
Version:        1.14.4
Release:        7
Summary:        Not well tested plugins for GStreamer framework
License:        LGPLv2+ and LGPLv2
URL:            http://gstreamer.freedesktop.org/
Source0:        https://gstreamer.freedesktop.org/src/gst-plugins-bad/gst-plugins-bad-%{version}.tar.xz

BuildRequires:  gstreamer1-devel >= %{version} gdb
BuildRequires:  gstreamer1-plugins-base-devel >= %{version}
BuildRequires:  check gettext-devel libXt-devel gtk-doc
BuildRequires:  gobject-introspection-devel >= 1.31.1
BuildRequires:  bzip2-devel exempi-devel gsm-devel 
BuildRequires:  lcms2-devel libexif-devel libiptcdata-devel
BuildRequires:  libnice-devel librsvg2-devel libsndfile-devel
BuildRequires:  mesa-libGL-devel mesa-libGLES-devel mesa-libGLU-devel
BuildRequires:  openssl-devel orc-devel libwayland-client-devel 
BuildRequires:  opus-devel nettle-devel libgcrypt-devel
BuildRequires:  gnutls-devel pkgconfig(gudev-1.0) pkgconfig(libusb-1.0)
BuildRequires:  gtk3-devel >= 3.4 bluez-libs-devel >= 5.0 libwebp-devel
BuildRequires:  mesa-libEGL-devel webrtc-audio-processing-devel

%if %{with extras}
BuildRequires:  libbs2b-devel >= 3.1.0 fluidsynth-devel libass-devel
BuildRequires:  libchromaprint-devel libcurl-devel game-music-emu-devel
BuildRequires:  libkate-devel libmodplug-devel libofa-devel libvdpau-devel
BuildRequires:  openal-soft-devel openjpeg2-devel slv2-devel wildmidi-devel
BuildRequires:  zbar-devel zvbi-devel OpenEXR-devel
%endif

%description
GStreamer is a pipeline-based multi media framework that links together a
wide variety of media processing systems to complete complex workflows, based
on graphs of filters which operate on media data.
This package contains plug-ins that are not tested well enough yet, or the code
is not of good enough quality.

%if %{with extras}
%package        extras
Summary:        Extra GStreamer "bad"(not well tested) plugins
Requires:       %{name} = %{version}-%{release}

%description    extras
This package (%{name}-extras) providess extra not-well-tested plugins for sources
, sinks and effects which are not used very much and require
additional libraries to be installed.

%package        fluidsynth
Summary:        GStreamer "bad"(not well tested) plugins fluidsynth plugin
Requires:       %{name} = %{version}-%{release}
Requires:       soundfont2-default

%description    fluidsynth
This package (%{name}-fluidsynth) provides the fluidsynth
plugin which allows playback of midi files.

%package        wildmidi
Summary:        GStreamer "bad"(not well tested) plugins wildmidi plugin
Requires:       %{name} = %{version}-%{release}

%description    wildmidi
This package (%{name}-wildmidi) provides the wildmidi plugin which allows playback
of midi files.
%endif

%package        devel
Summary:        Development files for the GStreamer media framework "bad" plugins
Requires:       %{name} = %{version}-%{release}
Requires:       gstreamer1-plugins-base-devel

%description    devel
This package provides the development files for GStreamer not-well-tested plugins.

%prep
%autosetup -n gst-plugins-bad-%{version}

%build
%configure --disable-silent-rules --disable-fatal-warnings \
    --with-package-name="openEuler GStreamer-plugins-bad package" \
    --with-package-origin="https://openeuler.org/en/building/download.html" \
    %{!?with_extras:--disable-fbdev --disable-decklink --disable-linsys} \
    --enable-debug --disable-static --enable-gtk-doc --enable-experimental \
    --disable-dts --disable-faac --disable-faad --disable-nas \
    --disable-mimic --disable-libmms --disable-mpeg2enc --disable-mplex \
    --disable-neon --disable-rtmp --disable-xvid \
    --disable-flite --disable-mpg123 --disable-sbc --disable-opencv \
    --disable-spandsp --disable-voamrwbenc --disable-x265
%make_build

%install
%make_install

install -d $RPM_BUILD_ROOT%{_datadir}/appdata
cat > $RPM_BUILD_ROOT%{_datadir}/appdata/gstreamer-bad-free.appdata.xml <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!-- Copyright 2013 Richard Hughes <richard@hughsie.com> -->
<component type="codec">
  <id>gstreamer-bad-free</id>
  <metadata_license>CC0-1.0</metadata_license>
  <name>GStreamer Multimedia Codecs - Extra</name>
  <summary>Multimedia playback for AIFF, DVB, GSM, MIDI, MXF and Opus</summary>
  <description>
    <p>
      This addon includes several additional codecs that are missing
      something - perhaps a good code review, some documentation, a set of
      tests, a real live maintainer, or some actual wide use.
      However, they might be good enough to play your media files.
    </p>
    <p>
      These codecs can be used to encode and decode media files where the
      format is not patent encumbered.
    </p>
    <p>
      A codec decodes audio and video for for playback or editing and is also
      used for transmission or storage.
      Different codecs are used in video-conferencing, streaming media and
      video editing applications.
    </p>
  </description>
  <keywords>
    <keyword>AIFF</keyword>
    <keyword>DVB</keyword>
    <keyword>GSM</keyword>
    <keyword>MIDI</keyword>
    <keyword>MXF</keyword>
    <keyword>Opus</keyword>
  </keywords>
  <url type="homepage">http://gstreamer.freedesktop.org/</url>
  <url type="bugtracker">https://bugzilla.gnome.org/enter_bug.cgi?product=GStreamer</url>
  <url type="help">http://gstreamer.freedesktop.org/documentation/</url>
  <url type="donation">http://www.gnome.org/friends/</url>
  <update_contact><!-- upstream-contact_at_email.com --></update_contact>
</component>
EOF
%find_lang gst-plugins-bad-%{majorminor}
%delete_la

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files -f gst-plugins-bad-%{majorminor}.lang
%license COPYING COPYING.LIB
%doc AUTHORS README REQUIREMENTS
%{_datadir}/appdata/*.appdata.xml
%{_datadir}/gstreamer-%{majorminor}/presets/GstFreeverb.prs
%{_libdir}/libgst*-%{majorminor}.so.*
%{_libdir}/girepository-1.0/Gst*-%{majorminor}.typelib

%{_libdir}/gstreamer-%{majorminor}/libgstaccurip.so
%{_libdir}/gstreamer-%{majorminor}/libgstadpcmdec.so
%{_libdir}/gstreamer-%{majorminor}/libgstadpcmenc.so
%{_libdir}/gstreamer-%{majorminor}/libgstaiff.so
%{_libdir}/gstreamer-%{majorminor}/libgstasfmux.so
%{_libdir}/gstreamer-%{majorminor}/libgstaudio{buffersplit,fxbad,latency,mixmatrix,visualizers}.so
%{_libdir}/gstreamer-%{majorminor}/libgstautoconvert.so
%{_libdir}/gstreamer-%{majorminor}/libgstbayer.so
%{_libdir}/gstreamer-%{majorminor}/libgstcamerabin.so
%{_libdir}/gstreamer-%{majorminor}/libgstcoloreffects.so
%{_libdir}/gstreamer-%{majorminor}/libgstcompositor.so
%{_libdir}/gstreamer-%{majorminor}/libgstdashdemux.so
%{_libdir}/gstreamer-%{majorminor}/libgstfaceoverlay.so
%if %{with extras}
%{_libdir}/gstreamer-%{majorminor}/libgstfbdevsink.so
%endif

%{_libdir}/gstreamer-%{majorminor}/libgstfestival.so
%{_libdir}/gstreamer-%{majorminor}/libgstfieldanalysis.so
%{_libdir}/gstreamer-%{majorminor}/libgstfreeverb.so
%{_libdir}/gstreamer-%{majorminor}/libgstfrei0r.so
%{_libdir}/gstreamer-%{majorminor}/libgstgaudieffects.so
%{_libdir}/gstreamer-%{majorminor}/libgstgdp.so
%{_libdir}/gstreamer-%{majorminor}/libgstgeometrictransform.so
%{_libdir}/gstreamer-%{majorminor}/libgstlegacyrawparse.so
%{_libdir}/gstreamer-%{majorminor}/libgstid3tag.so
%{_libdir}/gstreamer-%{majorminor}/libgstipcpipeline.so
%{_libdir}/gstreamer-%{majorminor}/libgstinter.so
%{_libdir}/gstreamer-%{majorminor}/libgstinterlace.so
%{_libdir}/gstreamer-%{majorminor}/libgstivfparse.so
%{_libdir}/gstreamer-%{majorminor}/libgstivtc.so
%{_libdir}/gstreamer-%{majorminor}/libgstjp2kdecimator.so
%{_libdir}/gstreamer-%{majorminor}/libgstjpegformat.so
%{_libdir}/gstreamer-%{majorminor}/libgstmidi.so
%{_libdir}/gstreamer-%{majorminor}/libgstmpeg{psdemux,tsdemux,psmux,tsmux}.so
%{_libdir}/gstreamer-%{majorminor}/libgstmxf.so
%{_libdir}/gstreamer-%{majorminor}/libgstnetsim.so
%{_libdir}/gstreamer-%{majorminor}/libgstpcapparse.so
%{_libdir}/gstreamer-%{majorminor}/libgstpnm.so
%{_libdir}/gstreamer-%{majorminor}/libgstproxy.so
%{_libdir}/gstreamer-%{majorminor}/libgstremovesilence.so
%{_libdir}/gstreamer-%{majorminor}/libgstrfbsrc.so
%{_libdir}/gstreamer-%{majorminor}/libgstrsvg.so
%{_libdir}/gstreamer-%{majorminor}/libgstrtponvif.so
%{_libdir}/gstreamer-%{majorminor}/libgstsdpelem.so
%{_libdir}/gstreamer-%{majorminor}/libgstsegmentclip.so
%{_libdir}/gstreamer-%{majorminor}/libgstshm.so
%{_libdir}/gstreamer-%{majorminor}/libgstsmooth.so
%{_libdir}/gstreamer-%{majorminor}/libgstsmoothstreaming.so
%{_libdir}/gstreamer-%{majorminor}/libgstspeed.so
%{_libdir}/gstreamer-%{majorminor}/libgststereo.so
%{_libdir}/gstreamer-%{majorminor}/libgstsubenc.so
%{_libdir}/gstreamer-%{majorminor}/libgsttimecode.so
%{_libdir}/gstreamer-%{majorminor}/libgstuvch264.so
%{_libdir}/gstreamer-%{majorminor}/libgstvideo{filtersbad,frame_audiolevel,parsersbad,signal}.so
%{_libdir}/gstreamer-%{majorminor}/libgstvmnc.so
%{_libdir}/gstreamer-%{majorminor}/libgstyadif.so
%{_libdir}/gstreamer-%{majorminor}/libgsty4mdec.so
%{_libdir}/gstreamer-%{majorminor}/libgstdvb.so
%{_libdir}/gstreamer-%{majorminor}/libgstvcdsrc.so
%{_libdir}/gstreamer-%{majorminor}/libgstbluez.so
%{_libdir}/gstreamer-%{majorminor}/libgstbz2.so
%{_libdir}/gstreamer-%{majorminor}/libgstcolormanagement.so
%{_libdir}/gstreamer-%{majorminor}/libgstdtls.so
%{_libdir}/gstreamer-%{majorminor}/libgsthls.so
%{_libdir}/gstreamer-%{majorminor}/libgstgsm.so
%{_libdir}/gstreamer-%{majorminor}/libgstkms.so
%{_libdir}/gstreamer-%{majorminor}/libgstopenglmixers.so
%{_libdir}/gstreamer-%{majorminor}/libgstopusparse.so
%{_libdir}/gstreamer-%{majorminor}/libgstsndfile.so
%{_libdir}/gstreamer-%{majorminor}/libgstttmlsubs.so
%{_libdir}/gstreamer-%{majorminor}/libgstwaylandsink.so
%{_libdir}/gstreamer-%{majorminor}/libgstwebp.so
%{_libdir}/gstreamer-%{majorminor}/libgstwebrtc.so
%{_libdir}/gstreamer-%{majorminor}/libgstwebrtcdsp.so
%{_libdir}/gstreamer-%{majorminor}/libgstdebugutilsbad.so
%{_libdir}/gstreamer-%{majorminor}/libgstdvbsuboverlay.so
%{_libdir}/gstreamer-%{majorminor}/libgstdvdspu.so
%{_libdir}/gstreamer-%{majorminor}/libgstsiren.so
%if ! %{with extras}
%exclude %{_libdir}/gstreamer-%{majorminor}/libgstcurl.so
%endif


%if %{with extras}
%files extras
%{_libdir}/gstreamer-%{majorminor}/libgstassrender.so
%{_libdir}/gstreamer-%{majorminor}/libgstbs2b.so
%{_libdir}/gstreamer-%{majorminor}/libgstchromaprint.so
%{_libdir}/gstreamer-%{majorminor}/libgstcurl.so
%{_libdir}/gstreamer-%{majorminor}/libgstdecklink.so
%{_libdir}/gstreamer-%{majorminor}/libgstgme.so
%{_libdir}/gstreamer-%{majorminor}/libgstkate.so
%{_libdir}/gstreamer-%{majorminor}/libgstmodplug.so
%{_libdir}/gstreamer-%{majorminor}/libgstofa.so
%{_libdir}/gstreamer-%{majorminor}/libgstopen{al,exr,jpeg}.so
%{_libdir}/gstreamer-%{majorminor}/libgstteletext.so
%{_libdir}/gstreamer-%{majorminor}/libgstvdpau.so
%{_libdir}/gstreamer-%{majorminor}/libgstzbar.so

%files fluidsynth
%{_libdir}/gstreamer-%{majorminor}/libgstfluidsynthmidi.so

%files wildmidi
%{_libdir}/gstreamer-%{majorminor}/libgstwildmidi.so
%endif

%files devel
%doc %{_datadir}/gtk-doc/html/gst-plugins-bad*-%{majorminor}
%{_datadir}/gir-1.0/Gst*-%{majorminor}.gir
%{_libdir}/libgst*-%{majorminor}.so
%{_libdir}/pkgconfig/gstreamer*-%{majorminor}.pc
%{_includedir}/gstreamer-%{majorminor}/gst/*

%changelog
* Tue May 19 2020 openEuler Buildteam <buildteam@openeuler.org> - 1.14.4-7
- rebuild for libwebp-1.1.0

* Sat Mar 21 2020 songnannan <songnannan2@huawei.com> - 1.14.4-6
- bugfix the unpackage file

* Thu Jan 23 2020 openEuler Buildteam <buildteam@openeuler.org> - 1.14.4-5
- Type:bugfix
- Id:NA
- SUG:NA
- DESC:delete the jasper

* Thu Jan 16 2020 zhujunhao <zhujunhao5@huawei.com> - 1.14.4-4
- Modify url and remove useless file

* Wed Jan 15 2020 openEuler Buildteam <buildteam@openeuler.org> - 1.14.4-3
- Type:enhancement
- Id:NA
- SUG:NA
- DESC:optimization the spec

* Tue Oct 22 2019 Alex Chao <zhaolei746@huawei.com> - 1.14.4-2
- Package init
