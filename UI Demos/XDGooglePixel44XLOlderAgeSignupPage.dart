import 'package:flutter/material.dart';
import './XDComponent11.dart';
import './XDGooglePixel44XLHomePage.dart';
import 'package:adobe_xd/page_link.dart';
import 'package:flutter_svg/flutter_svg.dart';

class XDGooglePixel44XLOlderAgeSignupPage extends StatelessWidget {
  XDGooglePixel44XLOlderAgeSignupPage({
    Key key,
  }) : super(key: key);
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xffffffff),
      body: Stack(
        children: <Widget>[
          Transform.translate(
            offset: Offset(35.0, 219.0),
            child: SizedBox(
              width: 308.0,
              height: 589.0,
              child: XDComponent11(),
            ),
          ),
          Transform.translate(
            offset: Offset(39.5, 0.5),
            child: SvgPicture.string(
              _svg_vjuw5,
              allowDrawingOutsideViewBox: true,
            ),
          ),
          Transform.translate(
            offset: Offset(0.0, 66.0),
            child: Container(
              width: 412.0,
              height: 102.0,
              decoration: BoxDecoration(
                borderRadius: BorderRadius.circular(8.0),
                color: const Color(0xffffffff),
                border: Border.all(width: 1.0, color: const Color(0xff707070)),
              ),
            ),
          ),
          Transform.translate(
            offset: Offset(164.0, 104.0),
            child: Text(
              'DigiPack',
              style: TextStyle(
                fontFamily: 'Segoe UI',
                fontSize: 20,
                color: const Color(0xff707070),
              ),
              textAlign: TextAlign.left,
            ),
          ),
          Transform.translate(
            offset: Offset(80.0, 321.0),
            child: SingleChildScrollView(
              child: Wrap(
                alignment: WrapAlignment.center,
                spacing: 24,
                runSpacing: 20,
                children: [
                  {
                    'text': 'First Name',
                  },
                  {
                    'text': 'Last Name',
                  },
                  {
                    'text': 'Email',
                  },
                  {
                    'text': 'Password',
                  },
                  {
                    'text': 'Confirm Password',
                  }
                ].map((map) {
                  final text = map['text'];
                  return Transform.translate(
                    offset: Offset(4.0, 0.0),
                    child: SizedBox(
                      width: 249.0,
                      height: 59.0,
                      child: Stack(
                        children: <Widget>[
                          Container(
                            width: 249.0,
                            height: 59.0,
                            decoration: BoxDecoration(
                              borderRadius: BorderRadius.circular(19.0),
                              color: const Color(0xffffffff),
                              border: Border.all(
                                  width: 1.0, color: const Color(0xff3389e8)),
                            ),
                          ),
                          Transform.translate(
                            offset: Offset(21.0, 22.0),
                            child: Text(
                              text,
                              style: TextStyle(
                                fontFamily: 'Segoe UI',
                                fontSize: 15,
                                color: const Color(0xff707070),
                              ),
                              textAlign: TextAlign.left,
                            ),
                          ),
                        ],
                      ),
                    ),
                  );
                }).toList(),
              ),
            ),
          ),
          Transform.translate(
            offset: Offset(179.0, 846.0),
            child: Container(
              width: 46.0,
              height: 13.0,
              decoration: BoxDecoration(
                borderRadius: BorderRadius.circular(8.0),
                color: const Color(0xff000000),
                border: Border.all(width: 1.0, color: const Color(0xff707070)),
              ),
            ),
          ),
          Transform.translate(
            offset: Offset(7.0, 0.0),
            child: Text(
              '4:21',
              style: TextStyle(
                fontFamily: 'Segoe UI',
                fontSize: 16,
                color: const Color(0xff707070),
              ),
              textAlign: TextAlign.left,
            ),
          ),
          Transform.translate(
            offset: Offset(-10.5, 23.5),
            child: SvgPicture.string(
              _svg_z2je1u,
              allowDrawingOutsideViewBox: true,
            ),
          ),
          Transform.translate(
            offset: Offset(164.0, 259.0),
            child: Text(
              'Sign Up!',
              style: TextStyle(
                fontFamily: 'Segoe UI',
                fontSize: 20,
                color: const Color(0xff707070),
              ),
              textAlign: TextAlign.left,
            ),
          ),
          Transform.translate(
            offset: Offset(69.0, 719.0),
            child: PageLink(
              links: [
                PageLinkInfo(
                  transition: LinkTransition.Fade,
                  ease: Curves.easeOut,
                  duration: 0.3,
                  pageBuilder: () => XDGooglePixel44XLHomePage(),
                ),
              ],
              child: Container(
                width: 274.0,
                height: 71.0,
                decoration: BoxDecoration(
                  borderRadius: BorderRadius.circular(19.0),
                  color: const Color(0xff3389e8),
                  border:
                      Border.all(width: 1.0, color: const Color(0xff3389e8)),
                ),
              ),
            ),
          ),
          Transform.translate(
            offset: Offset(139.0, 741.0),
            child: Text(
              'Create Account',
              style: TextStyle(
                fontFamily: 'Segoe UI',
                fontSize: 20,
                color: const Color(0xffffffff),
              ),
              textAlign: TextAlign.left,
            ),
          ),
        ],
      ),
    );
  }
}

const String _svg_vjuw5 =
    '<svg viewBox="39.5 0.5 333.0 870.0" ><path transform="translate(39.5, 0.5)" d="M 0 870 L 1 0" fill="none" stroke="#707070" stroke-width="1" stroke-miterlimit="4" stroke-linecap="butt" /><path transform="translate(372.5, 0.5)" d="M 0 870 L 0 0" fill="none" stroke="#707070" stroke-width="1" stroke-miterlimit="4" stroke-linecap="butt" /></svg>';
const String _svg_z2je1u =
    '<svg viewBox="-10.5 23.5 450.0 1.0" ><path transform="translate(-10.5, 23.5)" d="M 0 0 L 450 0" fill="none" stroke="#707070" stroke-width="1" stroke-miterlimit="4" stroke-linecap="butt" /></svg>';
