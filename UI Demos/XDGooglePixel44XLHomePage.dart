import 'package:flutter/material.dart';
import 'package:flutter_svg/flutter_svg.dart';

class XDGooglePixel44XLHomePage extends StatelessWidget {
  XDGooglePixel44XLHomePage({
    Key key,
  }) : super(key: key);
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xffffffff),
      body: Stack(
        children: <Widget>[
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
              'Home Page',
              style: TextStyle(
                fontFamily: 'Segoe UI',
                fontSize: 20,
                color: const Color(0xff707070),
              ),
              textAlign: TextAlign.left,
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
            offset: Offset(6.0, 0.0),
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
        ],
      ),
    );
  }
}

const String _svg_vjuw5 =
    '<svg viewBox="39.5 0.5 333.0 870.0" ><path transform="translate(39.5, 0.5)" d="M 0 870 L 1 0" fill="none" stroke="#707070" stroke-width="1" stroke-miterlimit="4" stroke-linecap="butt" /><path transform="translate(372.5, 0.5)" d="M 0 870 L 0 0" fill="none" stroke="#707070" stroke-width="1" stroke-miterlimit="4" stroke-linecap="butt" /></svg>';
const String _svg_z2je1u =
    '<svg viewBox="-10.5 23.5 450.0 1.0" ><path transform="translate(-10.5, 23.5)" d="M 0 0 L 450 0" fill="none" stroke="#707070" stroke-width="1" stroke-miterlimit="4" stroke-linecap="butt" /></svg>';
