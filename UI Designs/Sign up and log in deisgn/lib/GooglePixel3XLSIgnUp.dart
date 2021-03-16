import 'package:flutter/material.dart';
import 'dart:ui' as ui;
import 'package:adobe_xd/pinned.dart';
import 'package:flutter_svg/flutter_svg.dart';
import './GooglePixel3XLLogIn.dart';
import 'package:adobe_xd/page_link.dart';
import './GooglePixel3XLLogInSignUp.dart';

class GooglePixel3XLSIgnUp extends StatelessWidget {
  GooglePixel3XLSIgnUp({
    Key key,
  }) : super(key: key);
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xffffffff),
      body: Stack(
        children: <Widget>[
          Transform.translate(
            offset: Offset(-2.0, -33.0),
            child:
                // Adobe XD layer: '00-The-Endangered_H…' (shape)
                Container(
              width: 423.0,
              height: 880.0,
              decoration: BoxDecoration(
                image: DecorationImage(
                  image: const AssetImage('assets/images/blueBackground.jpg'),
                  fit: BoxFit.cover,
                  colorFilter: new ColorFilter.mode(
                      Colors.black.withOpacity(0.83), BlendMode.dstIn),
                ),
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
            offset: Offset(19.0, 23.0),
            child: SizedBox(
              width: 374.0,
              height: 801.0,
              child: Stack(
                children: <Widget>[
                  Pinned.fromSize(
                    bounds: Rect.fromLTWH(0.0, 0.0, 374.0, 801.0),
                    size: Size(374.0, 801.0),
                    pinLeft: true,
                    pinRight: true,
                    pinTop: true,
                    pinBottom: true,
                    child: Container(
                      decoration: BoxDecoration(
                        color: const Color(0xffffffff),
                        border: Border.all(
                            width: 0.5, color: const Color(0xffffffff)),
                      ),
                    ),
                  ),
                  Pinned.fromSize(
                    bounds: Rect.fromLTWH(45.3, 233.9, 289.4, 349.0),
                    size: Size(374.0, 801.0),
                    pinLeft: true,
                    pinRight: true,
                    fixedHeight: true,
                    child: SingleChildScrollView(
                      child: Wrap(
                        alignment: WrapAlignment.center,
                        spacing: 20,
                        runSpacing: 20,
                        children: [{}, {}, {}, {}, {}].map((map) {
                          return SizedBox(
                            width: 289.0,
                            height: 50.0,
                            child: Stack(
                              children: <Widget>[
                                SvgPicture.string(
                                  _svg_aod3s5,
                                  allowDrawingOutsideViewBox: true,
                                ),
                              ],
                            ),
                          );
                        }).toList(),
                      ),
                    ),
                  ),
                  Pinned.fromSize(
                    bounds: Rect.fromLTWH(156.0, 253.0, 62.0, 14.0),
                    size: Size(374.0, 801.0),
                    fixedWidth: true,
                    fixedHeight: true,
                    child: Text(
                      'First Name',
                      style: TextStyle(
                        fontFamily: 'Helvetica Neue',
                        fontSize: 12,
                        color: const Color(0xffcfd3d8),
                        fontWeight: FontWeight.w700,
                      ),
                      textAlign: TextAlign.center,
                    ),
                  ),
                  Pinned.fromSize(
                    bounds: Rect.fromLTWH(156.0, 323.0, 60.0, 14.0),
                    size: Size(374.0, 801.0),
                    fixedWidth: true,
                    fixedHeight: true,
                    child: Text(
                      'Last Name',
                      style: TextStyle(
                        fontFamily: 'Helvetica Neue',
                        fontSize: 12,
                        color: const Color(0xffcfd3d8),
                        fontWeight: FontWeight.w700,
                      ),
                      textAlign: TextAlign.center,
                    ),
                  ),
                  Pinned.fromSize(
                    bounds: Rect.fromLTWH(166.0, 393.0, 32.0, 14.0),
                    size: Size(374.0, 801.0),
                    fixedWidth: true,
                    fixedHeight: true,
                    child: Text(
                      'Email',
                      style: TextStyle(
                        fontFamily: 'Helvetica Neue',
                        fontSize: 12,
                        color: const Color(0xffcfd3d8),
                        fontWeight: FontWeight.w700,
                      ),
                      textAlign: TextAlign.center,
                    ),
                  ),
                  Pinned.fromSize(
                    bounds: Rect.fromLTWH(96.0, 689.0, 188.0, 14.0),
                    size: Size(374.0, 801.0),
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
                        'Already have an account? Login.',
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
                    bounds: Rect.fromLTWH(116.5, 709.5, 148.0, 1.0),
                    size: Size(374.0, 801.0),
                    pinBottom: true,
                    fixedWidth: true,
                    fixedHeight: true,
                    child: SvgPicture.string(
                      _svg_o70g1l,
                      allowDrawingOutsideViewBox: true,
                      fit: BoxFit.fill,
                    ),
                  ),
                  Container(),
                  Pinned.fromSize(
                    bounds: Rect.fromLTWH(54.0, 89.0, 272.0, 68.0),
                    size: Size(374.0, 801.0),
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
                  Pinned.fromSize(
                    bounds: Rect.fromLTWH(157.0, 463.0, 60.0, 14.0),
                    size: Size(374.0, 801.0),
                    fixedWidth: true,
                    fixedHeight: true,
                    child: Text(
                      'Password ',
                      style: TextStyle(
                        fontFamily: 'Helvetica Neue',
                        fontSize: 12,
                        color: const Color(0xffcfd3d8),
                        fontWeight: FontWeight.w700,
                      ),
                      textAlign: TextAlign.center,
                    ),
                  ),
                  Pinned.fromSize(
                    bounds: Rect.fromLTWH(132.0, 533.0, 110.0, 14.0),
                    size: Size(374.0, 801.0),
                    fixedWidth: true,
                    fixedHeight: true,
                    child: Text(
                      'Confirm Password ',
                      style: TextStyle(
                        fontFamily: 'Helvetica Neue',
                        fontSize: 12,
                        color: const Color(0xffcfd3d8),
                        fontWeight: FontWeight.w700,
                      ),
                      textAlign: TextAlign.center,
                    ),
                  ),
                ],
              ),
            ),
          ),
          Transform.translate(
            offset: Offset(70.0, 640.0),
            child:
                // Adobe XD layer: 'Button' (shape)
                Container(
              width: 281.0,
              height: 50.0,
              decoration: BoxDecoration(
                borderRadius: BorderRadius.circular(25.0),
                color: const Color(0xff5188ff),
              ),
            ),
          ),
          Transform.translate(
            offset: Offset(158.2, 658.0),
            child: SizedBox(
              width: 106.0,
              child: Text(
                'Create Account',
                style: TextStyle(
                  fontFamily: 'Helvetica Neue',
                  fontSize: 12,
                  color: const Color(0xffffffff),
                  fontWeight: FontWeight.w700,
                ),
                textAlign: TextAlign.center,
              ),
            ),
          ),
        ],
      ),
    );
  }
}

const String _svg_aod3s5 =
    '<svg viewBox="43.0 415.9 289.4 50.0" ><path transform="translate(43.0, 415.87)" d="M 2.024121999740601 0 L 287.4253234863281 0 C 288.5432434082031 0 289.4494323730469 0.8954304456710815 289.4494323730469 2 L 289.4494323730469 48 C 289.4494323730469 49.10456848144531 288.5432434082031 50 287.4253234863281 50 L 151.418701171875 50 L 2.024121999740601 50 C 0.9062302112579346 50 0 49.10456848144531 0 48 L 0 2 C 0 0.8954304456710815 0.9062302112579346 0 2.024121999740601 0 Z" fill="#ffffff" stroke="#8cbffd" stroke-width="1" stroke-miterlimit="4" stroke-linecap="butt" /></svg>';
const String _svg_o70g1l =
    '<svg viewBox="114.5 709.5 148.0 1.0" ><path transform="translate(114.47, 709.45)" d="M 0 0 L 148 0" fill="none" stroke="#8cbffd" stroke-width="2" stroke-miterlimit="4" stroke-linecap="butt" /></svg>';
