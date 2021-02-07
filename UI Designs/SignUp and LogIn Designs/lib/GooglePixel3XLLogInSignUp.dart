import 'package:flutter/material.dart';
import 'dart:ui' as ui;
import 'package:adobe_xd/pinned.dart';
import './GooglePixel3XLSIgnUp.dart';
import 'package:adobe_xd/page_link.dart';
import './GooglePixel3XLLogIn.dart';
import 'package:flutter_svg/flutter_svg.dart';

class GooglePixel3XLLogInSignUp extends StatelessWidget {
  GooglePixel3XLLogInSignUp({
    Key key,
  }) : super(key: key);
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xffffffff),
      body: Stack(
        children: <Widget>[
          // Adobe XD layer: '00-The-Endangered_H…' (shape)
          Container(
            width: 412.0,
            height: 847.0,
            decoration: BoxDecoration(
              image: DecorationImage(
                image: const AssetImage('assets/images/blueBackground.jpg'),
                fit: BoxFit.cover,
                colorFilter: new ColorFilter.mode(
                    Colors.black.withOpacity(0.83), BlendMode.dstIn),
              ),
            ),
          ),
          // Adobe XD layer: 'black overlay' (shape)
          ClipRect(
            child: BackdropFilter(
              filter: ui.ImageFilter.blur(sigmaX: 19.85, sigmaY: 19.85),
              child: Container(
                width: 411.0,
                height: 847.0,
                decoration: BoxDecoration(),
              ),
            ),
          ),
          Transform.translate(
            offset: Offset(18.0, 22.0),
            child: SizedBox(
              width: 371.0,
              height: 803.0,
              child: Stack(
                children: <Widget>[
                  Pinned.fromSize(
                    bounds: Rect.fromLTWH(0.0, 0.0, 371.0, 803.0),
                    size: Size(371.0, 803.0),
                    pinLeft: true,
                    pinRight: true,
                    pinTop: true,
                    pinBottom: true,
                    child: Container(
                      decoration: BoxDecoration(
                        color: const Color(0xffffffff),
                      ),
                    ),
                  ),
                  Pinned.fromSize(
                    bounds: Rect.fromLTWH(45.0, 323.0, 286.0, 50.0),
                    size: Size(371.0, 803.0),
                    pinLeft: true,
                    pinRight: true,
                    fixedHeight: true,
                    child:
                        // Adobe XD layer: 'Button' (shape)
                        Container(
                      decoration: BoxDecoration(
                        borderRadius: BorderRadius.circular(2.0),
                        color: const Color(0xffea4335),
                      ),
                    ),
                  ),
                  Pinned.fromSize(
                    bounds: Rect.fromLTWH(45.0, 407.0, 286.0, 50.0),
                    size: Size(371.0, 803.0),
                    pinLeft: true,
                    pinRight: true,
                    fixedHeight: true,
                    child:
                        // Adobe XD layer: 'Button' (shape)
                        PageLink(
                      links: [
                        PageLinkInfo(
                          transition: LinkTransition.Fade,
                          ease: Curves.easeOut,
                          duration: 0.3,
                          pageBuilder: () => GooglePixel3XLSIgnUp(),
                        ),
                      ],
                      child: Container(
                        decoration: BoxDecoration(
                          borderRadius: BorderRadius.circular(2.0),
                          color: const Color(0xfffce2a9),
                        ),
                      ),
                    ),
                  ),
                  Pinned.fromSize(
                    bounds: Rect.fromLTWH(130.0, 343.0, 116.0, 14.0),
                    size: Size(371.0, 803.0),
                    fixedWidth: true,
                    fixedHeight: true,
                    child: Text(
                      'Sign up with Google',
                      style: TextStyle(
                        fontFamily: 'Helvetica Neue',
                        fontSize: 12,
                        color: const Color(0xffffffff),
                        fontWeight: FontWeight.w700,
                      ),
                      textAlign: TextAlign.center,
                    ),
                  ),
                  Pinned.fromSize(
                    bounds: Rect.fromLTWH(135.0, 425.0, 106.0, 14.0),
                    size: Size(371.0, 803.0),
                    fixedWidth: true,
                    fixedHeight: true,
                    child: Text(
                      'Sign up with Email',
                      style: TextStyle(
                        fontFamily: 'Helvetica Neue',
                        fontSize: 12,
                        color: const Color(0xff000000),
                        fontWeight: FontWeight.w700,
                      ),
                      textAlign: TextAlign.center,
                    ),
                  ),
                  Pinned.fromSize(
                    bounds: Rect.fromLTWH(115.0, 691.0, 146.0, 14.0),
                    size: Size(371.0, 803.0),
                    pinBottom: true,
                    fixedWidth: true,
                    fixedHeight: true,
                    child: PageLink(
                      links: [
                        PageLinkInfo(
                          transition: LinkTransition.Fade,
                          ease: Curves.easeOut,
                          duration: 0.3,
                          pageBuilder: () => GooglePixel3XLLogIn(),
                        ),
                      ],
                      child: Text(
                        'I already have an account',
                        style: TextStyle(
                          fontFamily: 'Helvetica Neue',
                          fontSize: 12,
                          color: const Color(0xff000000),
                          fontWeight: FontWeight.w700,
                        ),
                        textAlign: TextAlign.center,
                      ),
                    ),
                  ),
                  Pinned.fromSize(
                    bounds: Rect.fromLTWH(47.0, 207.0, 282.0, 39.0),
                    size: Size(371.0, 803.0),
                    pinLeft: true,
                    pinRight: true,
                    fixedHeight: true,
                    child: Text(
                      'DigiPack\'s Moto',
                      style: TextStyle(
                        fontFamily: 'Roboto',
                        fontSize: 15,
                        color: const Color(0x72000000),
                        height: 1.3333333333333333,
                      ),
                      textAlign: TextAlign.center,
                    ),
                  ),
                  Pinned.fromSize(
                    bounds: Rect.fromLTWH(114.7, 711.5, 148.0, 1.0),
                    size: Size(371.0, 803.0),
                    pinBottom: true,
                    fixedWidth: true,
                    fixedHeight: true,
                    child: SvgPicture.string(
                      _svg_k3ami9,
                      allowDrawingOutsideViewBox: true,
                      fit: BoxFit.fill,
                    ),
                  ),
                  Container(),
                  Pinned.fromSize(
                    bounds: Rect.fromLTWH(54.0, 89.0, 269.0, 68.0),
                    size: Size(371.0, 803.0),
                    pinLeft: true,
                    pinRight: true,
                    pinTop: true,
                    fixedHeight: true,
                    child: Text(
                      'DIGIPACK',
                      style: TextStyle(
                        fontFamily: 'Roboto',
                        fontSize: 50,
                        color: const Color(0xff000000),
                        letterSpacing: 5,
                        fontWeight: FontWeight.w700,
                      ),
                      textAlign: TextAlign.left,
                    ),
                  ),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }
}

const String _svg_k3ami9 =
    '<svg viewBox="112.7 711.5 148.0 1.0" ><path transform="translate(112.69, 711.5)" d="M 0 0 L 148 0" fill="none" stroke="#8cbffd" stroke-width="2" stroke-miterlimit="4" stroke-linecap="butt" /></svg>';
